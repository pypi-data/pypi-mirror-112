# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mypy_clean_slate']

package_data = \
{'': ['*']}

install_requires = \
['autoflake>=1.4,<2.0',
 'black>=21.6b0,<22.0',
 'flake8-docstrings>=1.6.0,<2.0.0',
 'flake8-eradicate>=1.1.0,<2.0.0',
 'flake8-return>=1.1.3,<2.0.0',
 'flake8>=3.9.2,<4.0.0',
 'ipython>=7.25.0,<8.0.0',
 'isort>=5.9.2,<6.0.0',
 'mypy>=0.910,<0.911',
 'pre-commit>=2.13.0,<3.0.0',
 'pylint>=2.9.3,<3.0.0']

setup_kwargs = {
    'name': 'mypy-clean-slate',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'g',
    'author_email': 'g',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
