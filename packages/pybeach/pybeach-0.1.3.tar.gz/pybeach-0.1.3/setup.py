# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybeach', 'pybeach.support']

package_data = \
{'': ['*'], 'pybeach': ['classifiers/*']}

install_requires = \
['joblib>=1.0.1,<2.0.0', 'pandas>=1.3.0,<2.0.0', 'scikit-learn>=0.24.2,<0.25.0']

setup_kwargs = {
    'name': 'pybeach',
    'version': '0.1.3',
    'description': 'A Python package for locating the dune toe on cross-shore beach profile transects.',
    'long_description': None,
    'author': 'Tomas Beuzen',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
