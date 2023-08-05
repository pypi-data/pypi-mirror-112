# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sigma']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['sigma = sigma.cli:main']}

setup_kwargs = {
    'name': 'supersigma2-errorcodes',
    'version': '1.0',
    'description': 'A parser for DMC SuperSigma2 error codes',
    'long_description': '# supersigma2-errorcodes\n\nA python parser for DMC SuperSigma2 error codes.\n',
    'author': 'Thomas Feldmann',
    'author_email': 'mail@tfeldmann.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
