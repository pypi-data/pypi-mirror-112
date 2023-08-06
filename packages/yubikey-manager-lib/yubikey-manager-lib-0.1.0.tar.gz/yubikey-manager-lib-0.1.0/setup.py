# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['yubikey_manager_lib']
install_requires = \
['pyudev>=0.22.0,<0.23.0', 'yubikey-manager>=4.0.3,<5.0.0']

entry_points = \
{'console_scripts': ['ykman-repl = yubikey_manager_repl:main']}

setup_kwargs = {
    'name': 'yubikey-manager-lib',
    'version': '0.1.0',
    'description': 'Run yubikey-manager commands programmatically',
    'long_description': None,
    'author': 'Dick Marinus',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
