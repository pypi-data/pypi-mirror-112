# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magichttp', 'magichttp.h1impl']

package_data = \
{'': ['*']}

install_requires = \
['magicdict>=1.0.6,<2.0.0']

extras_require = \
{':python_version <= "3.7"': ['importlib-metadata>=4.0.1,<5.0.0']}

setup_kwargs = {
    'name': 'magichttp',
    'version': '1.1.2',
    'description': 'An http stack for asyncio.',
    'long_description': 'magichttp\n=========\n.. image:: https://github.com/futursolo/magichttp/actions/workflows/everything.yml/badge.svg\n    :target: https://github.com/futursolo/magichttp/actions/workflows/everything.yml\n\n.. image:: https://coveralls.io/repos/github/futursolo/magichttp/badge.svg?branch=master\n    :target: https://coveralls.io/github/futursolo/magichttp\n\n.. image:: https://img.shields.io/pypi/v/magichttp.svg\n    :target: https://pypi.org/project/magichttp/\n\nAsynchronous http, made easy.\n\nMagichttp is an http stack for asyncio, which provides one the ability to create\ntheir own async http client/server without diving into the http protocol\nimplementation.\n\nInstall\n-------\n\n.. code-block:: shell\n\n  $ pip install magichttp -U\n\n\nUsage\n-----\nSee :code:`examples/echo_client.py` and :code:`examples/echo_server.py`.\n\nUnder Development\n-----------------\nMagichttp is in beta. Basic unittests and contract checks are in place;\nhowever, it still may have unknown bugs. Bug reports and pull requests are\nalways welcomed.\n\nLicense\n-------\nCopyright 2021 Kaede Hoshikawa\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n',
    'author': 'Kaede Hoshikawa',
    'author_email': 'futursolo@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/futursolo/magichttp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
