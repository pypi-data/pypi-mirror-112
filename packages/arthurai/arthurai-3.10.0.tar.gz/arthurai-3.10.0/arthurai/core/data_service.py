import logging
import os
import tempfile
from typing import Dict, Optional, Any, TYPE_CHECKING, List

from pandas import DataFrame
import pandas as pd
import zipfile
import shutil
from pathlib import PurePath
import uuid

from arthurai.common.constants import Stage, InputType
from arthurai.common.exceptions import UserValueError
from arthurai.core import util
#  imports ArthurModel for type checking, required due to circular import
if TYPE_CHECKING:
    from arthurai.core.models import ArthurModel

logger = logging.getLogger(__name__)


class DatasetService:
    COUNTS = "counts"
    SUCCESS = "success"
    FAILURE = "failure"
    TOTAL = "total"
    FAILURES = "failures"
    DEFAULT_MAX_IMAGE_DATA_BYTES = 300000000  # 300 MB

    @staticmethod
    def convert_dataframe(model_id: str, stage: Optional[Stage], df: DataFrame) -> str:
        """Convert a dataframe to parquet named {model.id}-{stage}.parquet in the system tempdir

        :param model_id: a model id
        :param stage: the :py:class:`.Stage`
        :param df: the dataframe to convert

        Returns:
            The filename of the parquet file that was created
        """
        name = "{0}-{1}.parquet".format(model_id, stage) if stage else "{0}.parquet".format(model_id)
        filename = os.path.join(tempfile.mkdtemp(), name)
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

        df.to_parquet(filename, index=False, allow_truncated_timestamps=True)
        return filename

    
    @staticmethod
    def chunk_parquet_image_set(directory_path: str, image_attribute: str,
                                max_image_data_bytes: int = DEFAULT_MAX_IMAGE_DATA_BYTES) -> str:
        """Takes in a directory path with parquet files containing image attributes.
        Divides images up into 300MB chunks, then zipped, the parquet file is also split up to match.
        Parquet files will have random filename, and image zips will have matching name.

        """
        # make output dir for storing all chunks. At end will get:
        # tmp_dir/
        #    123.parquet, 123.zip, 456.parquet, 456.zip
        # TODO remove print statements, add logs to indicate processing, can take a while to run
        output_dir = tempfile.mkdtemp()
        files = util.retrieve_parquet_files(directory_path)
        if not files:
            raise UserValueError("The directory supplied does not contain any parquet files to upload")
        
        # loop through each parquet file
        for file in files:
            # keep track of where we are in parquet file, in case file needs to be split
            # to match image chunk
            cur_size = 0
            last_df_chunk_index = 0
            cur_img_dir = tempfile.mkdtemp(prefix=output_dir + "/")

            # this shouldn't happen, but check just in case
            if file.suffix != ".parquet":
                continue
            df = pd.read_parquet(file)

            if image_attribute not in df:
                # TODO should we raise exception here instead?
                logger.warning(f"Found parquet file missing image attribute, not including in reference set: {file.name}")
                continue
            
            # loop through each row in parquet file
            for cur_df_index, image_path in enumerate(df[image_attribute]):
                # verify image exists
                if not os.path.exists(image_path):
                    # TODO raise error here?
                    logger.warning(f"Image does not exist for row, not including in reference set: {image_path}")
                    continue
                
                # move image to temp dir
                image_path = PurePath(image_path)
                temp_image_path = os.path.join(cur_img_dir, image_path.name)
                shutil.copyfile(image_path, temp_image_path)
                img_bytes = os.path.getsize(temp_image_path)
                cur_size += img_bytes

                # if we have reached max image file size, save and start new chunk
                if cur_size >= max_image_data_bytes:
                    chunk_name = str(uuid.uuid4())

                    # create parquet chunk
                    df_chunk = df.iloc[last_df_chunk_index:cur_df_index + 1]
                    # replace image attribute with just the filename, no path
                    df_chunk[image_attribute] = df_chunk[image_attribute].apply(lambda x: PurePath(x).name)
                    df_chunk_filename = f"{chunk_name}.parquet"
                    df_chunk_path = os.path.join(output_dir, df_chunk_filename)
                    df_chunk.to_parquet(df_chunk_path)

                    # zip images
                    image_zip_path = os.path.join(output_dir, chunk_name)
                    shutil.make_archive(image_zip_path, 'zip', cur_img_dir)

                    # reset for next chunk
                    shutil.rmtree(cur_img_dir)
                    cur_img_dir = tempfile.mkdtemp(prefix=output_dir + "/")
                    cur_size = 0
                    last_df_chunk_index = cur_df_index + 1
            # we have reached end of current file, close off the current chunk before next parquet file
            # TODO maybe pull this into function so no repeated code, but so many things to pass in
            chunk_name = str(uuid.uuid4())

            # create parquet chunk
            df_chunk = df.iloc[last_df_chunk_index:cur_df_index + 1]
            # replace image attribute with just the filename, no path
            df_chunk[image_attribute] = df_chunk[image_attribute].apply(lambda x: PurePath(x).name)
            df_chunk_filename = f"{chunk_name}.parquet"
            df_chunk_path = os.path.join(output_dir, df_chunk_filename)
            df_chunk.to_parquet(df_chunk_path)

            # zip images
            image_zip_path = os.path.join(output_dir, chunk_name)
            shutil.make_archive(image_zip_path, 'zip', cur_img_dir)

            # clean up
            shutil.rmtree(cur_img_dir)
        return output_dir

    @staticmethod
    def send_parquet_files_from_dir_iteratively(model: 'ArthurModel', directory_path: str,
                                                url: str, upload_file_param_name: str,
                                                additional_form_params: Optional[Dict[str, Any]] = None,
                                                retries: int = 0):
        """Sends parquet files iteratively from a specified directory to a specified url for a given model

        :param retries: Number of times to retry the request if it results in a 400 or higher response code
        :param model:    the :py:class:`!arthurai.client.apiv2.model.ArthurModel`
        :param directory_path:    local path containing parquet files to send
        :param url:    POST url endpoint to send files to
        :param upload_file_param_name:     name to use in body with attached files
        :param additional_form_params: dictionary of additional form file params to send along with parquet file

        :raises MissingParameterError: the request failed

        :returns A list of files which failed to upload
        """
        files = util.retrieve_parquet_files(directory_path)
        if not files:
            raise UserValueError("The directory supplied does not contain any parquet files to upload")

        failed_files = []
        succeeded_files = []
        expected_keys = {DatasetService.SUCCESS, DatasetService.FAILURE, DatasetService.TOTAL}

        counts = {
            DatasetService.SUCCESS: 0,
            DatasetService.FAILURE: 0,
            DatasetService.TOTAL: 0
        }
        failures: List[Any] = []

        for file in files:
            if file.suffix == '.parquet':
                with open(file, 'rb') as parquet_file:
                    headers = {'Content-Type': 'multipart/form-data'}
                    form_parts = {} if additional_form_params is None else additional_form_params
                    form_parts.update({upload_file_param_name: parquet_file})

                    # add corresponding image data if image model
                    if model.input_type == InputType.Image:
                        # image zip file has same path and name as parquet file
                        image_zip_name = str(os.path.join(file.parent, file.stem)) + ".zip"
                        image_zip_file = open(image_zip_name, 'rb')
                        form_parts.update({'image_data': image_zip_file})

                    resp = model._client.post(url, data=None, files=form_parts, headers=headers,
                                              return_raw_response=True, retries=retries)
                    if resp.status_code == 201:
                        logger.info(f"Uploaded completed: {file}")
                        succeeded_files.append(file)
                    elif resp.status_code == 207:
                        logger.info(f"Upload completed: {file}")
                        result: Dict[str, Dict[str, int]] = resp.json()
                        # ensure the response is in the correct format
                        if DatasetService.COUNTS in result and DatasetService.FAILURES in result \
                                and set(result[DatasetService.COUNTS].keys()) == expected_keys:
                            counts[DatasetService.SUCCESS] += \
                                result[DatasetService.COUNTS][DatasetService.SUCCESS]
                            counts[DatasetService.FAILURE] += \
                                result[DatasetService.COUNTS][DatasetService.FAILURE]
                            counts[DatasetService.TOTAL] += \
                                result[DatasetService.COUNTS][DatasetService.TOTAL]
                            failures.append(result[DatasetService.FAILURES])
                        else:
                            failures.append(result)
                    else:
                        logger.error(f"Failed to upload file: {resp.text}")
                        failed_files.append(file)
                        failures.append(resp.json())
                        counts[DatasetService.FAILURE] += 1
                        counts[DatasetService.TOTAL] += 1
                # close image zip
                if model.input_type == InputType.Image:
                    image_zip_file.close()
                    try:
                        os.remove(image_zip_file.name)
                    except Exception:
                        logger.warning(f"Failed to delete temporary image file at {image_zip_file.name}")
                    

        file_upload_info = {
            DatasetService.COUNTS: counts,
            DatasetService.FAILURES: failures
        }

        # Only log failed or succeeded files if they exist
        if len(failed_files) > 0:
            logger.error(f'Failed to upload {len(failed_files)} files')
        if len(succeeded_files) > 0:
            logger.info(f'Successfully uploaded {len(succeeded_files)} files')
        return failed_files, file_upload_info


class ImageZipper:

    def __init__(self):
        self.temp_file = tempfile.NamedTemporaryFile()
        self.zip = zipfile.ZipFile(self.temp_file.name, 'w')

    def add_file(self, path: str):
        self.zip.write(path)

    def get_zip(self):
        self.zip.close()
        return self.temp_file

    def __del__(self):
        self.zip.close()
        self.temp_file.close()
