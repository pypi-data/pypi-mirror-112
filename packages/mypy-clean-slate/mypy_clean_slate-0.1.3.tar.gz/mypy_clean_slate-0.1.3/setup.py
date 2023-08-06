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

entry_points = \
{'console_scripts': ['mypy_clean_slate = mypy_clean_slate.main:main']}

setup_kwargs = {
    'name': 'mypy-clean-slate',
    'version': '0.1.3',
    'description': 'CLI tool for providing a clean slate for mypy usage within a project.',
    'long_description': '# Mypy Clean Slate\n\nCLI tool for providing a clean slate for mypy usage within a project\n\nIt can be difficult to get a large project to the point where `mypy --strict` can be run on it. Rather than incrementally increasing the severity, either overall or per module, `mypy_clean_slate` enables one to ignore all previous errors so that `mypy --strict` (or similar) can be used immediately.\n\n\n# Usage\n\n```\nusage: main.py [-h] [-n] [-r] [-a] [-o MYPY_REPORT_OUTPUT]\n\nCLI tool for providing a clean slate for mypy usage within a project.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -n, --none            Handle missing "-> None" hints on functions.\n  -r, --generate_mypy_error_report\n                        Generate \'mypy_error_report.txt\' in the cwd.\n  -a, --add_type_ignore\n                        Add "# type: ignore[<error-code>]" to suppress all raised mypy errors.\n  -o MYPY_REPORT_OUTPUT, --mypy_report_output MYPY_REPORT_OUTPUT\n                        File to save report output to (default is mypy_error_report.txt)\n```\n\nSee `./tests/test_mypy_clean_slate.py` for an example.\n\n# Issues\n\n## Handling lines with preexisting ignores.\n\nIf there are instances of `pylint: disable` or `noqa: ` ignores then these currently have\nto be handled separately. eg:\n\n```python\ndef add(a, b): # pylint: disable=invalid-name\n    return a + b\n```\n\nwould be manually rewritten as\n\n```python\ndef add(a, b): # type: ignore[no-untyped-def] # pylint: disable=invalid-name\n    return a + b\n```\n\n# TODO\n\n* handle there being different types of ignores (pylint/flake8/etc) already within the\n  code.\n',
    'author': 'George Lenton',
    'author_email': 'georgelenton@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/geo7/mypy_clean_slate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
