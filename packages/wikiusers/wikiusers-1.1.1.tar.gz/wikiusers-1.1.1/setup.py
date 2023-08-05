# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wikiusers',
 'wikiusers.dataloader',
 'wikiusers.logger',
 'wikiusers.postprocessor',
 'wikiusers.postprocessor.utils',
 'wikiusers.postprocessor.utils.elaborator',
 'wikiusers.rawprocessor',
 'wikiusers.rawprocessor.utils',
 'wikiusers.settings']

package_data = \
{'': ['*']}

install_requires = \
['autopep8>=1.5.7,<2.0.0',
 'joblib>=1.0.1,<2.0.0',
 'pylint>=2.9.3,<3.0.0',
 'pymongo>=3.11.4,<4.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'whdtscraper>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'wikiusers',
    'version': '1.1.1',
    'description': 'A python3 module that uses the Mediawiki History Dump Tsv to download the datasets, analyze them, uploading them to MongoDB and postprocess them. The result is a database with tons of information on every individual user of Wikipedia',
    'long_description': None,
    'author': 'Eugenio Vinicio Berretta',
    'author_email': 'euberdeveloper@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/euberdeveloper/wikiusers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
