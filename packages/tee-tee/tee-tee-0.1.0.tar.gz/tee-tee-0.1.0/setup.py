# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tee-tee']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.6b0,<22.0',
 'mypy>=0.910,<0.911',
 'pydantic>=1.8.2,<2.0.0',
 'quine-mccluskey>=0.3,<0.4']

setup_kwargs = {
    'name': 'tee-tee',
    'version': '0.1.0',
    'description': 'Truth table utility',
    'long_description': None,
    'author': 'Nick Rushton',
    'author_email': 'rushton.nicholas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
