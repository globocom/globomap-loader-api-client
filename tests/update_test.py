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
from unittest.mock import Mock
from unittest.mock import patch

import unittest2
from globomap_api_client.update import Update


class UpdateTest(unittest2.TestCase):

    def tearDown(self):
        patch.stopall()

    def test_post(self):
        update = Update(Mock())
        update.make_request = Mock()
        update.post({'doc': 1})

        update.make_request.assert_called_once_with(
            method='POST', uri='updates', data={'doc': 1})

    def test_list(self):
        update = Update(Mock())
        update.make_request = Mock()
        update.list()

        update.make_request.assert_called_once_with(
            method='GET', uri='updates')
