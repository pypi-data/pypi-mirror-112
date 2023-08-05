# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smsprofi_client']

package_data = \
{'': ['*']}

install_requires = \
['python-decouple>=3.4,<4.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'smsprofi-client',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'roci',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
