# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thlink_backend_deployment']

package_data = \
{'': ['*']}

install_requires = \
['aws-cdk.aws-lambda>=1.105.0,<2.0.0', 'aws-cdk.core>=1.105.0,<2.0.0']

setup_kwargs = {
    'name': 'thlink-backend-deployment',
    'version': '0.5.0',
    'description': '',
    'long_description': None,
    'author': 'thlink',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
