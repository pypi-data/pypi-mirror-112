# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dvenv', 'dvenv.commands']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'asgiref>=3.4.1,<4.0.0',
 'click>=8.0.1,<9.0.0',
 'redis>=3.5.3,<4.0.0',
 'sdist>=0.0.0,<0.0.1']

entry_points = \
{'console_scripts': ['dpython = dvenv:runner.python',
                     'dvenv = dvenv:main.main']}

setup_kwargs = {
    'name': 'dvenv',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Luke Lombardi',
    'author_email': 'luke@slai.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
