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
from globomap_loader_api_client.base import Base


class Update(Base):

    def post(self, document):
        """Send to API a document or a list of document.

        :param document: a document or a list of document.
        :type document: dict or list
        :return: Message with location of job
        :rtype: dict
        :raises ValidationError: if API returns status 400
        :raises Unauthorized: if API returns status 401
        :raises Forbidden: if API returns status 403
        :raises NotFound: if API returns status 404
        :raises ApiError: if API returns other status
        """

        if type(document) is dict:
            document = [document]

        return self.make_request(method='POST', uri='updates/', data=document)

    def get(self, key):
        """Return the status from a job.

        :param key: id of job
        :type document: dict or list
        :return: message with location of job
        :rtype: dict
        :raises Unauthorized: if API returns status 401
        :raises Forbidden: if API returns status 403
        :raises NotFound: if API returns status 404
        :raises ApiError: if API returns other status
        """

        uri = 'updates/job/{}'.format(key)
        return self.make_request(method='GET', uri=uri)
