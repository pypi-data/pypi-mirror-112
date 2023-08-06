# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pyidenticounter']
entry_points = \
{'console_scripts': ['pyicounter = pyidenticounter:main']}

setup_kwargs = {
    'name': 'pyidenticounter',
    'version': '0.2.0',
    'description': 'Count the number of identifier inside your python modules (variable, function, method and class names).',
    'long_description': None,
    'author': 'Bahram Aghaei',
    'author_email': 'aghaee.bahram@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
