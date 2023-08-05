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
    'version': '1.2',
    'description': 'A parser for DMC SuperSigma2 error codes',
    'long_description': '# supersigma2-errorcodes\n\nA python parser for DMC SuperSigma2 error codes.\n\n## Installation\n\nNeeds Python >= 3.6.\n\nInstall using `pip`:\n\n```\npip install supersigma2-errorcodes\n```\n\nIf you only need the standalone `sigma`-script to parse error codes in the command line,\nit is recommended to use `pipx` for the installation:\n\n```\npipx install supersigma2-errorcodes\n```\n\n## Command line usage\n\nA `sigma` command line script is installed by pip which can be used like this:\n\n```shell\n$ sigma 13.2 18.3 19.2\n[13.2] Accelerator more than 50% at power up: Wig-wag high at power up\n[18.3] High sided mosfets short circuit: M3 mosfets\n[19] Motor stall protection\n```\n\nIf no error codes are given, the usage is interactive.\n\n## Library usage\n\n```python\nfrom sigma import code_to_string\n\ncode_to_string("12.2")\n>>> "[12.2] Power up sequence fault: Traction: Forward switch active at power up"\n\ncode_to_string("18.3", include_code=False)\n>>> "High sided mosfets short circuit: M3 mosfets"\n```\n',
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
