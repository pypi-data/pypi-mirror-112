# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logging']

package_data = \
{'': ['*']}

install_requires = \
['corded>=1.3.8,<2.0.0', 'loguru>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'corded-logger',
    'version': '1.0.0',
    'description': 'A Discord webhook logger for Corded',
    'long_description': '# corded-logger\n\nA Discord webhook logger for Corded\n',
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
