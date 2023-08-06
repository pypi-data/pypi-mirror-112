# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tospip']

package_data = \
{'': ['*']}

install_requires = \
['Authlib==0.15.3',
 'Flask==1.1.2',
 'Jinja2==2.11.3',
 'MarkupSafe==1.1.1',
 'Werkzeug==1.0.1',
 'autopep8==1.5.7',
 'certifi==2020.12.5',
 'cffi==1.14.5',
 'chardet==3.0.4',
 'click==7.1.2',
 'colorama==0.4.4',
 'cryptography==3.4.6',
 'easygui==0.98.2',
 'et-xmlfile==1.1.0',
 'h11==0.12.0',
 'httpcore==0.12.3',
 'httpx==0.17.1',
 'idna==2.10',
 'itsdangerous==1.1.0',
 'lxml==4.6.2',
 'numpy==1.20.0',
 'oauthlib==3.1.0',
 'openpyxl==3.0.7',
 'pandas==1.2.3',
 'parse==1.19.0',
 'prompt-toolkit==3.0.17',
 'psutil==5.8.0',
 'pyOpenSSL==20.0.1',
 'pycodestyle==2.7.0',
 'pycparser==2.20',
 'pynput==1.7.3',
 'python-dateutil==2.8.1',
 'pytz==2021.1',
 'pywin32==301',
 'requests-oauthlib==1.3.0',
 'requests==2.25.1',
 'rfc3986==1.4.0',
 'selenium==3.141.0',
 'six==1.15.0',
 'sniffio==1.2.0',
 'td-ameritrade-python-api==0.3.5',
 'tda-api==1.3.3',
 'urllib3==1.26.4',
 'wcwidth==0.2.5',
 'websocket-client==0.58.0',
 'websockets==9.1',
 'xlwings>=0.24.2,<0.25.0']

setup_kwargs = {
    'name': 'tospip',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Nick Bean',
    'author_email': 'nickbean2255@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
