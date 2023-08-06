# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blackarrow', 'blackarrow.test']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.6b0,<22.0',
 'coveralls>=3.1.0,<4.0.0',
 'fabulous>=0.4.0,<0.5.0',
 'pytest-cov>=2.12.1,<3.0.0',
 'pytest>=6.2.4,<7.0.0',
 'twine>=3.4.1,<4.0.0']

setup_kwargs = {
    'name': 'blackarrow',
    'version': '1.0.9',
    'description': '',
    'long_description': None,
    'author': 'Zoe Farmer',
    'author_email': 'zoe@dataleek.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
