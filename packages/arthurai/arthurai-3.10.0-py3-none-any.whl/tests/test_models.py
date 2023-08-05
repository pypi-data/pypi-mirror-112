from datetime import datetime, timezone
from mock import patch, mock_open

import numpy as np
import pandas as pd
import pytest
import responses

from arthurai import ArthurAI
from arthurai.common.constants import ValueType, Stage, InputType, OutputType, ImageResponseType, ImageContentType
from arthurai.core.attributes import AttributeCategory, AttributeBin, ArthurAttribute
from arthurai.core.models import ArthurModel
import arthurai.core.util as core_util
from arthurai.common.exceptions import UserValueError, MethodNotApplicableError
from tests.base_test import BaseTest
from tests.test_request_models.fixtures import model_response_json_strings


class TestArthurModel(BaseTest):
    @responses.activate
    def test_send_parquet_file(self):
        input_dict = {
            "attr1": np.Inf,
            "attr2": "string1",
            "attr3": 3.44,
            "attr4": True,
            "attr5": np.nan,
            "attr6": -np.inf,
            "attr7": "string2",
            "attr8": None,
            "attr9": "",
            "attr10": np.inf,
        }
        expected_dict = {
            "attr1": None,
            "attr2": "string1",
            "attr3": 3.44,
            "attr4": True,
            "attr5": None,
            "attr6": None,
            "attr7": "string2",
            "attr8": None,
            "attr9": "",
            "attr10": None,
        }
        output_dict = ArthurModel._replace_nans_and_infinities_in_dict(input_dict)
        assert expected_dict == output_dict

    def test_replace_nans_none_type(self):
        output_dict = ArthurModel._replace_nans_and_infinities_in_dict(None)
        assert output_dict is None

    def test_standardize_pd_obj_for_nans(self):
        input_df = pd.DataFrame(
            [
                [1, 2, 3., 4, 5, 6, np.inf, np.nan, 1, 1],
                [7, 8, 9., 1, 2, 3, np.nan, -np.inf, 2, 2],
                [4, 5.5, 9., -np.inf, np.nan, np.Inf, np.nan, np.nan, np.nan, np.nan],
            ],
            columns = ["x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9"]
        )
        expected_df = pd.DataFrame(
            [
                [1, 2, 3., 4, 5, 6, np.nan, np.nan, 1, 1],
                [7, 8, 9., 1, 2, 3, np.nan, np.nan, 2, 2],
                [4, 5.5, 9., np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            ],
            columns = ["x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9"]
        )
        expected_df.x3 = expected_df.x3.astype(pd.Int64Dtype())
        expected_df.x4 = expected_df.x4.astype(pd.Int64Dtype())
        expected_df.x5 = expected_df.x5.astype(pd.Int64Dtype())

        attributes = {
            "x3": ValueType.Integer,
            "x4": ValueType.Integer,
            "x5": ValueType.Integer,
            "x8": ValueType.Float,
        }

        assert expected_df.equals(
            core_util.standardize_pd_obj(input_df, dropna=False, replacedatetime=False, attributes=attributes)
        )
        with pytest.raises(ValueError):
            assert expected_df.equals(
                core_util.standardize_pd_obj(input_df, dropna=True, replacedatetime=False, attributes=attributes)
            )  

    def test_standardize_pd_obj_for_series(self):
        input_series = [
            pd.Series([1, 2, 3]),
            pd.Series([1., 2., 3.]),
            pd.Series([1, 2, np.Inf], name="x1"),
            pd.Series([1, 2, np.Inf], name="x1"),
            pd.Series([1, 2, np.Inf], name="x1"),
            pd.Series([np.nan, -np.inf, np.inf]),
        ]
        input_attributes = [
            {},
            None,
            {"x1": ValueType.Integer},
            {"x1": ValueType.Float},
            {"x2": ValueType.Integer},
            {}
        ]
        expected_undropped_series = [
            pd.Series([1, 2, 3]),
            pd.Series([1., 2., 3.]),
            pd.Series([1, 2, np.nan]).astype(pd.Int64Dtype()),
            pd.Series([1, 2, np.nan]),
            pd.Series([1, 2, np.nan]),
            pd.Series([np.nan, np.nan, np.nan]),
        ]
        expected_dropped_series = [
            pd.Series([1, 2, 3]),
            pd.Series([1., 2., 3.]),
            pd.Series([1, 2]).astype(pd.Int64Dtype()),
            pd.Series([1, 2.]),
            pd.Series([1, 2.]),
            pd.Series([]),
        ]

        for inp, inp_attributes, exp_undropped, exp_dropped in zip(input_series, input_attributes, expected_undropped_series, expected_dropped_series):
            print(inp_attributes)
            assert exp_undropped.equals(
                core_util.standardize_pd_obj(inp, dropna=False, replacedatetime=False, attributes=inp_attributes)
            )
            assert exp_dropped.equals(
                core_util.standardize_pd_obj(inp, dropna=True, replacedatetime=False, attributes=inp_attributes)
            )

    def test_standardize_pd_obj_bad_input(self):
        for inp in ["string", "", 123, [1,2,3], {"key": "value"}]:
            with pytest.raises(TypeError):
                core_util.standardize_pd_obj(inp, dropna=True, replacedatetime=False)

    def test_standardize_pd_obj_for_datetimes(self):
        unaware_timestamp = datetime(2021, 2, 8, 12, 10, 5)
        aware_timestamp = datetime(2021, 2, 8, 12, 10, 5, tzinfo=timezone.utc)
        timestamp_to_expected_output = (
            (unaware_timestamp, ValueError),
            (aware_timestamp, "2021-02-08T12:10:05Z"),
        )

        for timestamp, expected_output in timestamp_to_expected_output:
            if isinstance(expected_output, str):
                actual_output = core_util.standardize_pd_obj(pd.Series([timestamp]), dropna=False, replacedatetime=True)
                assert expected_output == actual_output.values[0]
            else:
                with pytest.raises(expected_output):
                    core_util.standardize_pd_obj(pd.Series([timestamp]), dropna=False, replacedatetime=True)

    def test_add_attribute_with_categories(self):
        model = ArthurModel.from_json(model_response_json_strings[2])
        model.add_attribute(
            name="test_categorical_1",
            value_type=ValueType.Integer,
            stage=Stage.ModelPipelineInput,
            categorical=True,
            categories=[1, 2, 3, 4],
        )
        attr = model.get_attribute(name="test_categorical_1")
        assert len(attr.categories) == 4
        assert isinstance(attr.categories[0], AttributeCategory)

        model.add_attribute(
            name="test_categorical_2",
            value_type=ValueType.Integer,
            stage=Stage.ModelPipelineInput,
            categorical=True,
            categories=[AttributeCategory(value="hello")],
        )
        attr = model.get_attribute(name="test_categorical_2")
        assert len(attr.categories) == 1
        assert isinstance(attr.categories[0], AttributeCategory)
        assert attr.categories[0].value == "hello"

    def test_add_attribute_with_bins(self):
        model = ArthurModel.from_json(model_response_json_strings[2])
        model.add_attribute(
            name="test_bins_1",
            value_type=ValueType.Integer,
            stage=Stage.ModelPipelineInput,
            categorical=True,
            bins=[None, 10, 15, 20, None],
        )
        attr = model.get_attribute(name="test_bins_1")
        assert len(attr.bins) == 4
        assert isinstance(attr.bins[0], AttributeBin)
        assert attr.bins[0].continuous_start is None
        assert attr.bins[0].continuous_end == 10

        model.add_attribute(
            name="test_bins_2",
            value_type=ValueType.Integer,
            stage=Stage.ModelPipelineInput,
            categorical=True,
            bins=[
                AttributeBin(continuous_start=None, continuous_end=10),
                AttributeBin(continuous_start=10, continuous_end=15),
                AttributeBin(continuous_start=15, continuous_end=20),
            ],
        )
        attr = model.get_attribute(name="test_bins_2")
        assert len(attr.bins) == 3
        assert isinstance(attr.bins[0], AttributeBin)
        assert attr.bins[0].continuous_start is None
        assert attr.bins[0].continuous_end == 10

    def test_add_nlp_attribute(self):
        model = ArthurModel(
            partner_model_id="test",
            client=None,
            input_type=InputType.NLP,
            output_type=OutputType.Multiclass,
        )
        ref_data = pd.DataFrame(
            {"input_text": ["hello", "hi", "what's up", "yo", "cool"],}
        )
        model.from_dataframe(ref_data, stage=Stage.ModelPipelineInput)

        assert (
            model.get_attribute("input_text").value_type == ValueType.Unstructured_Text
        )
        assert model.get_attribute("input_text").categories is None

    def test_all_null_column(self):
        model = ArthurModel(
            partner_model_id="test",
            client=None,
            input_type=InputType.NLP,
            output_type=OutputType.Multiclass,
        )
        df = pd.DataFrame({'col1': [1], 'col2': [float("nan")]})
        model.from_dataframe(df, stage=Stage.ModelPipelineInput)

        expected_attributes = [
            ArthurAttribute(name='col1', value_type=ValueType.Integer, stage=Stage.ModelPipelineInput, position=0,
                            categorical=True, categories=[AttributeCategory(value='1', label=None)], is_unique=False),
            ArthurAttribute(name='col2', value_type=ValueType.Float, stage=Stage.ModelPipelineInput, position=1,
                            categorical=False, is_unique=False)]

        assert model.attributes == expected_attributes

    def test_nonzero_index_column(self):
        model = ArthurModel(
            partner_model_id="test",
            client=None,
            input_type=InputType.NLP,
            output_type=OutputType.Multiclass,
        )
        df = pd.DataFrame({'col1': [1], 'col2': [float("nan")]})
        df.index = [5]
        model.from_dataframe(df, stage=Stage.ModelPipelineInput)

        expected_attributes = [
            ArthurAttribute(name='col1', value_type=ValueType.Integer, stage=Stage.ModelPipelineInput, position=0,
                            categorical=True, categories=[AttributeCategory(value='1', label=None)], is_unique=False),
            ArthurAttribute(name='col2', value_type=ValueType.Float, stage=Stage.ModelPipelineInput, position=1,
                            categorical=False, is_unique=False)]

        assert model.attributes == expected_attributes

    def test_set_categorical_value_labels(self):
        model = ArthurModel.from_json(model_response_json_strings[2])
        model.add_attribute(
            name="test_categorical_1",
            value_type=ValueType.Integer,
            stage=Stage.ModelPipelineInput,
            categorical=True,
            categories=[1, 2],
        )
        expected_categories = {1: "Male", 2: "Female"}
        model.set_attribute_labels("test_categorical_1", labels=expected_categories)
        cats = model.get_attribute("test_categorical_1").categories
        for category in cats:
            assert int(category.value) in expected_categories
            assert expected_categories[int(category.value)] == category.label

    @responses.activate
    def test_get_image(self):
        client = ArthurAI(access_key=self.access_key, url=self._base_url, offline=True)
        model = ArthurModel(client=client.client,
                            partner_model_id="test",
                            input_type=InputType.Image,
                            output_type=OutputType.Multiclass)
        model.id = '1234567890abcdef'
        image_id = '0a1b2c3d4e5f9687'
        path = '.'
        type = ImageResponseType.RawImage
        file_ext = '.png'
        response_content = 'content'.encode()
        expected_image_file = f"{path}/{type}_{image_id}{file_ext}"

        self.mockGet(f"/api/v3/models/{model.id}/inferences/images/{image_id}?type={type}", response_content, content_type=ImageContentType.Png)
        open_mock = mock_open()
        with patch("arthurai.core.models.open", open_mock, create=True):
            resulting_file = model.get_image(image_id, path, type=type)

        assert resulting_file == expected_image_file
        open_mock.assert_called_with(expected_image_file, 'wb')
        open_mock.return_value.write.assert_called_once_with(response_content)


    def test_add_object_detection_output_attributes(self):
        model = ArthurModel(
            partner_model_id="test",
            client=None,
            input_type=InputType.Image,
            output_type=OutputType.Multiclass,
        )

        # cannot call without proper types
        with pytest.raises(MethodNotApplicableError):
            model.add_object_detection_output_attributes('pred', 'gt', ['class_1', 'class_2'])
        model.input_type = InputType.NLP
        model.output_type = OutputType.ObjectDetection
        with pytest.raises(MethodNotApplicableError):
            model.add_object_detection_output_attributes('pred', 'gt', ['class_1', 'class_2'])

        # cannot call without classes
        model.output_type = OutputType.ObjectDetection
        model.input_type = InputType.Image
        with pytest.raises(UserValueError):
            model.add_object_detection_output_attributes('pred', 'gt', [])
        
        # names cannot match
        with pytest.raises(UserValueError):
            model.add_object_detection_output_attributes('pred', 'pred', ['class_1', 'class_2'])

        # happy path
        model.add_object_detection_output_attributes('pred', 'gt', ['class_1', 'class_2'])
        assert model.get_attribute('pred').value_type == ValueType.BoundingBox
        assert model.get_attribute('gt').value_type == ValueType.BoundingBox
        assert model.image_class_labels == ['class_1', 'class_2']