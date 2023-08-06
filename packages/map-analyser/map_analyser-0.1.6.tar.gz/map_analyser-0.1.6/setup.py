# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['app',
 'lib',
 'map_analyser',
 'map_analyser.app',
 'map_analyser.lib',
 'map_analyser.mapanalyser',
 'map_analyser.maplib',
 'mapanalyser',
 'maplib']

package_data = \
{'': ['*']}

install_requires = \
['Mosek>=9.2.37,<10.0.0',
 'Pillow>=8.1.0,<9.0.0',
 'cvxopt>=1.2.5,<2.0.0',
 'cvxpy>=1.1.10,<2.0.0',
 'func-timeout>=4.3.5,<5.0.0',
 'numpy>=1.20.1,<2.0.0',
 'pyclipper>=1.2.1,<2.0.0',
 'scipy>=1.6.0,<2.0.0',
 'sect>=0.5.0,<0.6.0',
 'tripy>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['cli_script = map_analyser.__main__:main']}

setup_kwargs = {
    'name': 'map-analyser',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'Simon Navratil',
    'author_email': 'navratil.simon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maischon/Bc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
