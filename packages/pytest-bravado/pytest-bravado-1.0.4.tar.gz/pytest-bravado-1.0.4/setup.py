# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pytest_bravado']
install_requires = \
['bravado>=11.0.2,<12.0.0']

entry_points = \
{'pytest11': ['bravado = pytest_bravado']}

setup_kwargs = {
    'name': 'pytest-bravado',
    'version': '1.0.4',
    'description': 'Pytest-bravado automatically generates from OpenAPI specification client fixtures.',
    'long_description': None,
    'author': 'Viktor Kutepov',
    'author_email': 'vkytepov@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vkutepov/pytest-bravado',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
