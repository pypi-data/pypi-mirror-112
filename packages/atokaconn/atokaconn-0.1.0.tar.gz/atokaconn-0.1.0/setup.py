# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atokaconn']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=8.10.1,<9.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'atokaconn',
    'version': '0.1.0',
    'description': 'A package that facilitates connections to and data extractions from the ATOKA API service.',
    'long_description': None,
    'author': 'guglielmo',
    'author_email': 'guglielmo@openpolis.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
