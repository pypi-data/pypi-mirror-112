# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cointanalysis']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.0,<2.0.0',
 'scikit-learn>=0.23,<0.25',
 'statsmodels>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'cointanalysis',
    'version': '0.3.4',
    'description': 'Python package for cointegration analysis.',
    'long_description': None,
    'author': 'Shota Imaki',
    'author_email': 'shota.imaki.0801@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.13,<4.0.0',
}


setup(**setup_kwargs)
