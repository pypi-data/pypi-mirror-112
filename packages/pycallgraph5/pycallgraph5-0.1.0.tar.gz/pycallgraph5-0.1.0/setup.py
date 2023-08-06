# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycallgraph']

package_data = \
{'': ['*']}

install_requires = \
['aiocontextvars>=0.2.2,<0.3.0',
 'atomicwrites>=1.3.0,<2.0.0',
 'contextvars>=2.4,<3.0',
 'loguru>=0.5.3,<0.6.0',
 'pyvis>=0.1.9,<0.2.0',
 'win32-setctime>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'pycallgraph5',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'BuRny',
    'author_email': 'gamingburny@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
