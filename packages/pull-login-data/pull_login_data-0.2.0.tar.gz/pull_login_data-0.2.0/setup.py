# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pull_login_data']
setup_kwargs = {
    'name': 'pull-login-data',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'ZacHooper',
    'author_email': 'zac.g.hooper@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
