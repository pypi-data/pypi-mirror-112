# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['stepshift']
install_requires = \
['PyMonad>=2.4.0,<3.0.0', 'pandas>=1.2.4,<2.0.0']

setup_kwargs = {
    'name': 'stepshift',
    'version': '0.3.0',
    'description': 'Time-step shifting modelling logic, used by the ViEWS team for training models.',
    'long_description': None,
    'author': 'peder2911',
    'author_email': 'pglandsverk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
