# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lodis_py']

package_data = \
{'': ['*']}

install_requires = \
['mugen>=0.5.0,<0.6.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'lodis-py',
    'version': '0.1.0',
    'description': 'lodis-py - A Lodis Python Sync/Async Client',
    'long_description': '# lodis-py - A Lodis Python Sync/Async Client\n',
    'author': 'PeterDing',
    'author_email': 'dfhayst@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lodis-org/lodis-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
