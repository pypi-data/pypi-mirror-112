# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['patchutils']
setup_kwargs = {
    'name': 'patchutils',
    'version': '1.1.1',
    'description': 'A simple utility for working with patches on strings',
    'long_description': None,
    'author': 'xcodz-dot',
    'author_email': '71920621+xcodz-dot@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xcodz-dot/patchutils',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
