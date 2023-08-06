# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['binteger']
setup_kwargs = {
    'name': 'binteger',
    'version': '0.10.0',
    'description': 'Binary integer representation toolkit',
    'long_description': None,
    'author': 'Aleksei Udovenko',
    'author_email': 'aleksei@affine.group',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
