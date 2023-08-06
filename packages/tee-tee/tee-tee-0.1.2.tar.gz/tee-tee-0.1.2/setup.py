# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tee_tee']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'quine-mccluskey>=0.3,<0.4', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['tt = tee_tee.main:run']}

setup_kwargs = {
    'name': 'tee-tee',
    'version': '0.1.2',
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
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
