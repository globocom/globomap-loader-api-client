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
import logging

import requests

from globomap_loader_api_client import exceptions


class Auth(object):
    """Module to make authentication in API."""

    logger = logging.getLogger(__name__)

    def __init__(self, api_url, username, password):
        """Make request in API to generate a token.

        :param api_url: URL of API
        :param username: username of API
        :param password: password of API
        :raises ValidationError: if API returns status 400
        :raises Unauthorized: if API returns status 401
        :raises ApiError: if API returns other status
        """

        self.api_url = api_url
        self.username = username
        self.password = password
        self.generate_token()

    def generate_token(self):
        """Make request in API to generate a token."""

        response = self._make_request()
        self.auth = response
        self.token = response['token']

    def _get_headers(self):
        return {
            'Content-Type': 'application/json'
        }

    def _make_request(self):
        try:
            url = '{}/v2/auth/'.format(self.api_url)
            data = {
                'username': self.username,
                'password': self.password
            }
            response = requests.post(
                url, data=json.dumps(data), headers=self._get_headers()
            )

        except Exception:
            self.logger.exception('Error in request')
            raise exceptions.ApiError('Error in request')

        else:
            return self._parser_response(response)

    def _parser_response(self, response):
        content = response.json()
        status_code = response.status_code

        if status_code == 200:
            return content
        elif status_code == 400:
            raise exceptions.ValidationError(content, status_code)
        elif status_code == 401:
            raise exceptions.Unauthorized(content, status_code)
        else:
            raise exceptions.ApiError(content, status_code)
