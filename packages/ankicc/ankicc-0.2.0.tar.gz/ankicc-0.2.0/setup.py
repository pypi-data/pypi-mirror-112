# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ankicc']

package_data = \
{'': ['*']}

install_requires = \
['OpenCC>=1.1.2,<2.0.0', 'ankipandas>=0.3.10,<0.4.0']

entry_points = \
{'console_scripts': ['ankicc = ankicc.console:run']}

setup_kwargs = {
    'name': 'ankicc',
    'version': '0.2.0',
    'description': 'Conversion anki flashcards between Traditional and Simplified Chinese',
    'long_description': None,
    'author': 'kaiiiz',
    'author_email': 'ukaizheng@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
