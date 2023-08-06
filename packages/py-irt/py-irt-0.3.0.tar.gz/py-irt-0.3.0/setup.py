# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_irt', 'py_irt.models']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.3,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pyro-ppl>=1.6.0,<2.0.0',
 'rich>=9.3.0,<10.0.0',
 'scikit-learn>=0.24.2,<0.25.0',
 'scipy>=1.6.3,<2.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['py-irt = py_irt.cli:app']}

setup_kwargs = {
    'name': 'py-irt',
    'version': '0.3.0',
    'description': 'Bayesian IRT models in Python',
    'long_description': None,
    'author': 'John P. Lalor',
    'author_email': 'john.lalor@nd.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
