# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hacktcha', 'hacktcha.generator']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.7.0,<0.8.0',
 'aiohttp>=3.7.4,<4.0.0',
 'captcha>=0.3,<0.4',
 'fastai>=2.3,<3.0',
 'fire>=0.4.0,<0.5.0',
 'numpy>=1.21.0,<2.0.0',
 'pillow>=8.2,<9.0',
 'sanic>=21.6.0,<22.0.0',
 'torch>=1.7.1,<2.0.0',
 'uuid>=1.30,<2.0']

setup_kwargs = {
    'name': 'hacktcha',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'zillionare',
    'author_email': 'code@jieyu.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.9,<4.0.0',
}


setup(**setup_kwargs)
