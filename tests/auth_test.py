"""
   Copyright 2018 Globo.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import json
from mock import MagicMock
from mock import patch

import unittest2

from globomap_loader_api_client import exceptions
from globomap_loader_api_client.auth import Auth


class AuthTest(unittest2.TestCase):

    TARGET = 'globomap_loader_api_client.auth.requests'

    def tearDown(self):
        patch.stopall()

    def test_generate_token(self):
        mock_requests = patch(self.TARGET).start()
        token_data = {
            'token': 'token123',
            'expires_at': '2018-04-12T05:51:58.144271Z',
        }
        response_mock = MagicMock(return_value=token_data)
        mock_requests.post.return_value = MagicMock(
            json=response_mock, status_code=200)
        Auth('http://localhost', 'test', '123')

        data = {
            'username': 'test',
            'password': '123'
        }
        headers = {
            'Content-Type': 'application/json'
        }
        mock_requests.post.assert_called_once_with(
            'http://localhost/v2/auth/', data=json.dumps(data), headers=headers
        )

    def test_generate_token_validator(self):
        mock_requests = patch(self.TARGET).start()

        response_mock = MagicMock(return_value={'message': 'Error'})
        mock_requests.post.return_value = MagicMock(
            json=response_mock, status_code=400)

        with self.assertRaises(exceptions.ValidationError):
            Auth('http://localhost', 'test', '123')

    def test_generate_token_unauthorized(self):
        mock_requests = patch(self.TARGET).start()

        response_mock = MagicMock(return_value={'message': 'Error'})
        mock_requests.post.return_value = MagicMock(
            json=response_mock, status_code=401)

        with self.assertRaises(exceptions.Unauthorized):
            Auth('http://localhost', 'test', '123')

    def test_generate_token_error(self):
        mock_requests = patch(self.TARGET).start()

        response_mock = MagicMock(return_value={'message': 'Error'})
        mock_requests.post.return_value = MagicMock(
            json=response_mock, status_code=500)

        with self.assertRaises(exceptions.ApiError):
            Auth('http://localhost', 'test', '123')

    def test_generate_token_exception(self):
        mock_requests = patch(self.TARGET).start()

        mock_requests.post = MagicMock(side_effect=Exception())

        with self.assertRaises(exceptions.ApiError):
            Auth('http://localhost', 'test', '123')
