# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rlc', 'rlc.xml']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xml-builder',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Rafa Leblic',
    'author_email': 'rafa@notin.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
