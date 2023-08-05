# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['test-poetry-publish']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'test-poetry-publish',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Nikia',
    'author_email': 'barinov.nikita49@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
