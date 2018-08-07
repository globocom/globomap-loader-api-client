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

from requests import Session

from globomap_loader_api_client import exceptions


class Base(object):

    logger = logging.getLogger(__name__)

    def __init__(self, auth, driver_name, retries=3):
        self.auth = auth
        self.driver_name = driver_name
        self.retries = retries
        self.session = Session()

    def _get_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'x-driver-name': self.driver_name,
            'Authorization': 'Token token={}'.format(self.auth.token)
        }
        return headers

    def make_request(self, method, uri, data=None, retries=0):
        request_url = '{}/v2/{}'.format(self.auth.api_url, uri)
        if type(data) is dict or type(data) is list:
            data = json.dumps(data)
        headers = self._get_headers()
        try:
            if method == 'GET':
                response = self.session.request(
                    method,
                    request_url,
                    headers=headers
                )
            else:
                response = self.session.request(
                    method,
                    request_url,
                    data=data,
                    headers=headers
                )
            self.logger.info('REQUEST: %s %s' % (method, request_url))
        except Exception:
            self.logger.exception('Error in request')
            raise exceptions.ApiError('Error in request')

        else:

            try:
                content = response.json()
            except json.JSONDecodeError:
                content = response.text
            status_code = response.status_code

            try:
                return self._parser_response(content, status_code)

            except exceptions.Unauthorized as err:

                if retries < self.retries:
                    self.auth.generate_token()
                    return self.make_request(
                        method=method, uri=uri, data=data, retries=retries + 1)

                self.logger.error('Unauthorized %s %s.', content, status_code)
                raise exceptions.Unauthorized(err.message, err.status_code)

            except exceptions.ApiError as err:

                if retries < self.retries:
                    return self.make_request(
                        method=method, uri=uri, data=data, retries=retries + 1)

                self.logger.error('ApiError %s %s.', content, status_code)
                raise exceptions.ApiError(err.message, err.status_code)

    def _parser_response(self, content, status_code):

        if status_code in (200, 202):
            self.logger.debug('Success %s %s.', content, status_code)
            return content
        elif status_code == 400:
            self.logger.error('ValidationError %s %s.', content, status_code)
            raise exceptions.ValidationError(content, status_code)
        elif status_code == 401:
            self.logger.warning('Unauthorized %s %s.', content, status_code)
            raise exceptions.Unauthorized(content, status_code)
        elif status_code == 403:
            self.logger.error('Forbidden %s %s.', content, status_code)
            raise exceptions.Forbidden(content, status_code)
        elif status_code == 404:
            self.logger.error('NotFound %s %s.', content, status_code)
            raise exceptions.NotFound(content, status_code)
        else:
            self.logger.warning('ApiError %s %s.', content, status_code)
            raise exceptions.ApiError(content, status_code)
