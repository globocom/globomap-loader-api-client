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
from mock import Mock
from mock import patch

import unittest2

from globomap_loader_api_client import exceptions
from globomap_loader_api_client.base import Base


class BaseTest(unittest2.TestCase):

    TARGET = 'globomap_loader_api_client.base.Session'

    def tearDown(self):
        patch.stopall()

    def test_post_error(self):
        mock_requests = patch(self.TARGET).start()
        response_mock = MagicMock(return_value={'message': 'Error'})

        mock_requests.return_value.request.return_value = MagicMock(
            json=response_mock, status_code=500)

        data = {'key': 'value'}
        base = Base(Mock(), 'driver_test')

        with self.assertRaises(exceptions.ApiError):
            base.make_request('POST', 'path', data)

    def test_post_exception(self):
        mock_requests = patch(self.TARGET).start()

        mock_requests.return_value.request.side_effect = Exception()

        data = {'key': 'value'}
        base = Base(Mock(), 'driver_test')

        with self.assertRaises(exceptions.ApiError):
            base.make_request('POST', 'path', data)

    def test_post_202(self):
        mock_session = patch(self.TARGET).start()

        response_mock = MagicMock(return_value={'message': 'message'})
        request_mock = mock_session.return_value.request
        request_mock.return_value = MagicMock(
            json=response_mock, status_code=202)

        data = {'key': 'value'}

        base = Base(Mock(api_url='http://localhost', token='token123'),
                    'driver_test')
        base.make_request('POST', 'path', data)

        headers = {
            'Content-Type': 'application/json',
            'x-driver-name': 'driver_test',
            'Authorization': 'Token token=token123'
        }
        request_mock.assert_called_once_with(
            'POST', 'http://localhost/v2/path', data=json.dumps(data), headers=headers
        )

    def test_post_400(self):
        mock_requests = patch(self.TARGET).start()
        response_mock = MagicMock(return_value={'message': 'Error'})

        mock_requests.return_value.request.return_value = MagicMock(
            json=response_mock, status_code=400)

        with self.assertRaises(exceptions.ValidationError):
            base = Base(Mock(), 'driver_test')
            data = {'key': 'value'}
            base.make_request('POST', 'path', data)

    def test_post_401(self):
        mock_requests = patch(self.TARGET).start()
        mock_time = patch(
            'globomap_loader_api_client.base.time').start()
        response_mock = MagicMock(return_value={'message': 'Error'})

        mock_requests.return_value.request.return_value = MagicMock(
            json=response_mock, status_code=401)

        data = {'key': 'value'}
        auth = Mock()
        auth.generate_token.return_value = Mock()
        base = Base(auth, 'driver_test', 4)
        mock_time.sleep.return_value = 1

        with self.assertRaises(exceptions.Unauthorized):
            base.make_request('GET', 'path', data)

        mock_time.sleep.assert_any_call(5 + 0)
        mock_time.sleep.assert_any_call(5 + 5)
        mock_time.sleep.assert_any_call(5 + 10)
        mock_time.sleep.assert_any_call(5 + 15)

    def test_post_403(self):
        mock_requests = patch(self.TARGET).start()
        response_mock = MagicMock(return_value={'message': 'Error'})

        mock_requests.return_value.request.return_value = MagicMock(
            json=response_mock, status_code=403)

        data = {'key': 'value'}
        base = Base(Mock(), 'driver_test')

        with self.assertRaises(exceptions.Forbidden):
            base.make_request('POST', 'path', None, data)

    def test_post_404(self):
        mock_requests = patch(self.TARGET).start()
        response_mock = MagicMock(return_value={'message': 'Error'})

        mock_requests.return_value.request.return_value = MagicMock(
            json=response_mock, status_code=404)

        data = {'key': 'value'}
        base = Base(Mock(), 'driver_test')

        with self.assertRaises(exceptions.NotFound):
            base.make_request('POST', 'path', None, data)

    def test_get_error(self):
        mock_requests = patch(self.TARGET).start()
        response_mock = MagicMock(return_value={'message': 'Error'})

        mock_requests.return_value.request.return_value = MagicMock(
            json=response_mock, status_code=500)

        base = Base(Mock(), 'driver_test')

        with self.assertRaises(exceptions.ApiError):
            base.make_request('GET', 'path', None)

    def test_get_exception(self):
        mock_requests = patch(self.TARGET).start()

        mock_requests.return_value.request.side_effect = Exception()
        base = Base(Mock(), 'driver_test')

        with self.assertRaises(exceptions.ApiError):
            base.make_request('GET', 'path', None)

    def test_get_200(self):
        mock_session = patch(self.TARGET).start()

        response_mock = MagicMock(return_value={'message': 'message'})
        request_mock = mock_session.return_value.request
        request_mock.return_value = MagicMock(
            json=response_mock, status_code=200)

        base = Base(Mock(api_url='http://localhost', token='token123'),
                    'driver_test')
        base.make_request('GET', 'path', None)

        headers = {
            'Content-Type': 'application/json',
            'x-driver-name': 'driver_test',
            'Authorization': 'Token token=token123'
        }
        request_mock.assert_called_once_with(
            'GET', 'http://localhost/v2/path', headers=headers
        )

    def test_get_401(self):
        mock_requests = patch(self.TARGET).start()
        mock_time = patch(
            'globomap_loader_api_client.base.time').start()
        response_mock = MagicMock(return_value={'message': 'Error'})

        mock_requests.return_value.request.return_value = MagicMock(
            json=response_mock, status_code=401)

        auth = Mock()
        auth.generate_token.return_value = Mock()
        base = Base(auth, 'driver_test', 3)
        mock_time.sleep.return_value = 1

        with self.assertRaises(exceptions.Unauthorized):
            base.make_request('GET', 'path', None)
        mock_time.sleep.assert_any_call(5 + 0)
        mock_time.sleep.assert_any_call(5 + 5)
        mock_time.sleep.assert_any_call(5 + 10)

    def test_get_403(self):
        mock_requests = patch(self.TARGET).start()
        response_mock = MagicMock(return_value={'message': 'Error'})

        mock_requests.return_value.request.return_value = MagicMock(
            json=response_mock, status_code=403)

        base = Base(Mock(), 'driver_test')

        with self.assertRaises(exceptions.Forbidden):
            base.make_request('GET', 'path', None)

    def test_get_404(self):
        mock_requests = patch(self.TARGET).start()
        response_mock = MagicMock(return_value={'message': 'Error'})

        mock_requests.return_value.request.return_value = MagicMock(
            json=response_mock, status_code=404)

        base = Base(Mock(), 'driver_test')

        with self.assertRaises(exceptions.NotFound):
            base.make_request('GET', 'path', None)
