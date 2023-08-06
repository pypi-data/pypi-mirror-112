# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rashsetup',
 'rashsetup.RashScrappers',
 'rashsetup.RashScrappers.RashScrappers',
 'rashsetup.RashScrappers.RashScrappers.spiders',
 'rashsetup.RashScrappers.RashScrappers.spiders.temp.Rashq07rkp57',
 'rashsetup.RashScrappers.RashScrappers.spiders.temp.Rashq07rkp57.Rash',
 'rashsetup.RashScrappers.RashScrappers.spiders.temp.Rashqz5_73ks',
 'rashsetup.RashScrappers.RashScrappers.spiders.temp.Rashqz5_73ks.Rash']

package_data = \
{'': ['*'],
 'rashsetup.RashScrappers': ['RashScrappers/spiders/temp/*',
                             'RashScrappers/spiders/temp/Rashq07rkp57/Rash.egg-info/*',
                             'RashScrappers/spiders/temp/Rashq07rkp57/Rash/Misc/Gifs/*',
                             'RashScrappers/spiders/temp/Rashq07rkp57/Rash/Misc/HTML/*',
                             'RashScrappers/spiders/temp/Rashq07rkp57/Rash/Misc/Icons/*',
                             'RashScrappers/spiders/temp/Rashq07rkp57/Rash/Misc/sql/*',
                             'RashScrappers/spiders/temp/Rashqz5_73ks/Rash.egg-info/*',
                             'RashScrappers/spiders/temp/Rashqz5_73ks/Rash/Misc/Gifs/*',
                             'RashScrappers/spiders/temp/Rashqz5_73ks/Rash/Misc/HTML/*',
                             'RashScrappers/spiders/temp/Rashqz5_73ks/Rash/Misc/Icons/*',
                             'RashScrappers/spiders/temp/Rashqz5_73ks/Rash/Misc/sql/*']}

setup_kwargs = {
    'name': 'rashsetup',
    'version': '0.3.0',
    'description': 'Setup Module that can be used for both testing Rash and also Setting up Rash',
    'long_description': None,
    'author': 'Rahul',
    'author_email': 'saihanumarahul66@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
