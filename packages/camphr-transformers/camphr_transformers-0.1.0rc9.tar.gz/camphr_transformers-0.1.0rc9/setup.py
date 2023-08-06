# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['camphr_transformers']

package_data = \
{'': ['*']}

install_requires = \
['camphr==0.10.0rc1', 'transformers>=4.8,<5.0']

extras_require = \
{'torch': ['torch>=1.8.0,<2.0.0']}

setup_kwargs = {
    'name': 'camphr-transformers',
    'version': '0.1.0rc9',
    'description': '',
    'long_description': None,
    'author': 'Yohei Tamura',
    'author_email': 'tamuhey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
