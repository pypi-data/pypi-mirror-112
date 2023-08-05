# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['corgy', 'tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'corgy',
    'version': '1.0.0b2',
    'description': 'Elegant command line parsing',
    'long_description': '# corgy\n\nElegant command line parsing for Python.\n',
    'author': 'Jayanth Koushik',
    'author_email': 'jnkoushik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jayanthkoushik/corgy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
