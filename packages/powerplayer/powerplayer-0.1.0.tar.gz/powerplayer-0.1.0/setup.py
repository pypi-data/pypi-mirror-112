# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['powerplayer']
install_requires = \
['bs4>=0.0.1,<0.0.2',
 'click-help-colors>=0.9.1,<0.10.0',
 'click>=8.0.1,<9.0.0',
 'pafy>=0.5.5,<0.6.0',
 'playsound>=1.2.2,<2.0.0',
 'python-vlc>=3.0.12118,<4.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['pplay = powerplayer:main']}

setup_kwargs = {
    'name': 'powerplayer',
    'version': '0.1.0',
    'description': 'A command line interface to play music',
    'long_description': '',
    'author': 'Avanindra Chakraborty',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AvanindraC/Powerplayer',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
