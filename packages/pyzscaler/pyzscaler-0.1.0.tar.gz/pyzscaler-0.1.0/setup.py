# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyzscaler', 'pyzscaler.zpa']

package_data = \
{'': ['*']}

install_requires = \
['python-box>=5.3.0,<6.0.0', 'restfly>=1.4.0,<2.0.0']

setup_kwargs = {
    'name': 'pyzscaler',
    'version': '0.1.0',
    'description': 'A python SDK for Zscaler.',
    'long_description': 'pyZscaler is an unofficial SDK for interacting with Zscaler APIs\n=====================================================================\npyZscaler aims to provide a uniform and easy-to-use interface for each of the Zscaler product APIs.\n\n\n.. attention:: This SDK is not affiliated with, nor supported by Zscaler in any way.\n\n   :strong:`Caveats`\n\n   - Not all features may be implemented.\n   - Implemented features may be buggy or incorrect.\n   - Bugs will be fixed in my own time.\n\nOverview\n==========\nWith each Zscaler product having its own developer documentation and authentication methods, this SDK should simplify\nyour ability to develop software that uses the Zscaler API.\n\nThis SDK leverages the very awesome `RESTfly framework <https://restfly.readthedocs.io/en/latest/index.html>`_ developed by Steve McGrath, which simplifies the development of\nbuilding libraries to interact with RESTful APIs. A big thank you to Steve.\n\nFeatures\n----------\n- Simplified authentication with Zscaler APIs.\n- Uniform interaction with all Zscaler APIs.\n- Uses `python-box <https://github.com/cdgriffith/Box/wiki>`_ to add dot notation access to json data structures.\n- Zscaler API output automatically converted from CamelCase to Snake Case.\n\nProducts\n---------\n- Zscaler Private Access (ZPA)\n- Zscaler Internet Access (ZIA) - (work in progress)\n- Cloud Security Posture Management (CSPM) - (work in progress)\n\nInstallation\n==============\n\nThe most recent version can be installed from pypi as per below.\n\n.. code-block:: console\n\n    $ pip install pyzscaler\n\nUsage\n========\nBefore you can interact with any of the Zscaler APIs, you will need to generate API keys for each product that you are\nwriting code for. Once you have generated the API keys and installed pyZscaler, you\'re ready to go.\n\nGetting started with ZPA\n--------------------------\nFor ZPA, you will need the ``CLIENT_ID``, ``CLIENT_SECRET`` and ``CUSTOMER_ID``.\n\n- `How to generate the CLIENT_ID, CLIENT_SECRET and find the CUSTOMER_ID <https://help.zscaler.com/zpa/about-api-keys>`_\n\n.. code-block:: python\n\n    from pyzscaler import ZPA\n    zpa = ZPA(\'CLIENT_ID\', \'CLIENT_SECRET\', \'CUSTOMER_ID\')\n    for app_segment in zpa.app_segments.list():\n        pprint(app_segment)\n\n\nLicense\n=========\nMIT License\n\nCopyright (c) 2021 Mitch Kelly\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.',
    'author': 'Mitch Kelly',
    'author_email': 'me@mkelly.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mitchos/pyZscaler',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
