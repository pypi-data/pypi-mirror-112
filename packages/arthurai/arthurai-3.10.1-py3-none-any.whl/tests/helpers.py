import json
from datetime import datetime
from unittest.mock import MagicMock

import pytz
import responses

from tests.fixtures.mocks import BASE_URL


CONTENT_TYPE_JSON = 'application/json'


def mock_post(append_url, dict_to_return, status=200):
    """
    Adds a mock 200 response

    :param append_url: the url to the base url
    :param dict_to_return: the dictionary to return as json
    :return: None
    """

    responses.add(responses.POST, BASE_URL + append_url,
                  json.dumps(dict_to_return), status=status,
                  content_type=CONTENT_TYPE_JSON)


def mock_patch(append_url, dict_to_return, status=200):
    """
    Adds a mock 200 response

    :param append_url: the url to the base url
    :param dict_to_return: the dictionary to return as json
    :return: None
    """

    responses.add(responses.PATCH, BASE_URL + append_url,
                  json.dumps(dict_to_return), status=status,
                  content_type=CONTENT_TYPE_JSON)


def mock_get(append_url, response_body, status=200, content_type=CONTENT_TYPE_JSON):
    """
    Adds a mock 200 response

    :param append_url: the url to the base url
    :param response_content: the response_content to return from the mock API request
    :return: None
    """

    responses.add(responses.GET,
                  BASE_URL + append_url,
                  body=json.dumps(response_body),
                  status=status,
                  content_type=content_type)


class MockShortUUID:
    def __init__(self, ids=None):
        if ids is None:
            self.ids = []
        else:
            self.ids = ids
        self.next_idx = 0

    def call_count(self):
        return self.next_idx

    def next(self):
        value = self.ids[self.next_idx]
        self.next_idx += 1
        return value


class MockDatetime:
    def __init__(self, return_vals=None, return_raw_strings=False):
        if return_vals is None or len(return_vals) == 0:
            self.timestamps = []
        else:
            if isinstance(return_vals[0], datetime):
                self.timestamps = return_vals
            elif isinstance(return_vals[0], str):
                mocks = []
                for ts in return_vals:
                    if return_raw_strings:
                        mocks.append(ts)
                    else:
                        dt = MagicMock(datetime)
                        dt.isoformat.return_value = ts
                        mocks.append(dt)
                self.timestamps = mocks
        self.next_idx = 0

    def call_count(self):
        return self.next_idx

    def next(self, tz):
        if tz != pytz.utc:
            raise ValueError("unexpected timezone")
        value = self.timestamps[self.next_idx]
        self.next_idx += 1
        return value
