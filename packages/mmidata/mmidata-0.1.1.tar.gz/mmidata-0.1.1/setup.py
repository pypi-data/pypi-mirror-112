# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mmidata', 'mmidata.utils']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.107,<2.0.0', 'humanize>=3.10.0,<4.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['mmidata = mmidata.main:cli']}

setup_kwargs = {
    'name': 'mmidata',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Dan Sikes',
    'author_email': 'dan@methodmi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
