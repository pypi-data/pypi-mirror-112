# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pcmap']

package_data = \
{'': ['*']}

install_requires = \
['ccmap>=2.1.3,<3.0.0',
 'docopt>=0.6.2,<0.7.0',
 'numpy>=1.20.3,<2.0.0',
 'pypstruct>=0.1,<0.2']

setup_kwargs = {
    'name': 'pcmap',
    'version': '0.2.1',
    'description': 'Computing contact map for protein structures',
    'long_description': None,
    'author': 'Guillaume Launay',
    'author_email': 'guillaume.launay@ibcp.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
