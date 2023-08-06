# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fitter_python']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'desert>=2020.11.18,<2021.0.0',
 'marshmallow>=3.12.1,<4.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['fitter-python = fitter_python.console:main']}

setup_kwargs = {
    'name': 'fitter-python',
    'version': '0.1.0',
    'description': 'A fitter Python project',
    'long_description': '# Fitter, happier python\n\nBased on the [hypermodern-python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/) series.\n\n[![Tests](https://github.com/anthonyjatoba/fitter-python/workflows/Tests/badge.svg)](https://github.com/anthonyjatoba/fitter-python/actions?workflow=Tests)\n[![codecov](https://codecov.io/gh/anthonyjatoba/fitter-python/branch/main/graph/badge.svg?token=U39TD5TDDI)](https://codecov.io/gh/anthonyjatoba/fitter-python)\n',
    'author': 'Anthony Jatobá',
    'author_email': 'anthonyjatoba@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/anthonyjatoba/fitter-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
