# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['rtd_poetry']
setup_kwargs = {
    'name': 'rtd-poetry-tmp',
    'version': '0.1.2',
    'description': 'Execute poetry install with dev dependencies on RTD',
    'long_description': None,
    'author': 'Chris Hunt',
    'author_email': 'chrahunt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
