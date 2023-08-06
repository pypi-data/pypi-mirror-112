# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yubikey-manager-lib', 'yubikey-manager-lib.test']

package_data = \
{'': ['*'],
 'yubikey-manager-lib': ['.git/*',
                         '.git/hooks/*',
                         '.git/info/*',
                         '.git/logs/*',
                         '.git/logs/refs/heads/*',
                         '.git/logs/refs/remotes/origin/*',
                         '.git/objects/06/*',
                         '.git/objects/09/*',
                         '.git/objects/15/*',
                         '.git/objects/1c/*',
                         '.git/objects/3c/*',
                         '.git/objects/52/*',
                         '.git/objects/54/*',
                         '.git/objects/5c/*',
                         '.git/objects/73/*',
                         '.git/objects/92/*',
                         '.git/objects/98/*',
                         '.git/objects/a1/*',
                         '.git/objects/ba/*',
                         '.git/objects/c0/*',
                         '.git/objects/c1/*',
                         '.git/refs/heads/*',
                         '.git/refs/remotes/origin/*']}

install_requires = \
['pyudev>=0.22.0,<0.23.0', 'yubikey-manager>=4.0.3,<5.0.0']

entry_points = \
{'console_scripts': ['ykman-repl = yubikey_manager_repl:main']}

setup_kwargs = {
    'name': 'yubikey-manager-lib',
    'version': '0.1.2',
    'description': 'Run yubikey-manager commands programmatically',
    'long_description': None,
    'author': 'Dick Marinus',
    'author_email': None,
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
