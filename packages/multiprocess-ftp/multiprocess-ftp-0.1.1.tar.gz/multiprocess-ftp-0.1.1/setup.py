# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multiprocess_ftp']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.105,<2.0.0', 'ftputil>=5.0.1,<6.0.0']

setup_kwargs = {
    'name': 'multiprocess-ftp',
    'version': '0.1.1',
    'description': 'FTP client library',
    'long_description': None,
    'author': 'Chris K',
    'author_email': 'chrisk60331@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
