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
from setuptools import setup

VERSION = __import__('globomap_loader_api_client').__version__

setup(
    name='globomap-loader-api-client',
    version=VERSION,
    description='Client to GloboMAP Loader API',
    author='Ederson Brilhante',
    author_email='ederson.brilhante@corp.globo.com',
    install_requires=[
        'requests==2.20.0'
    ],
    url='https://github.com/globocom/globomap-loader-api-client',
    packages=['globomap_loader_api_client'],
    package_data={'globomap_loader_api_client': ['*.py']},
)
