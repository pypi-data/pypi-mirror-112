# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lbcgo', 'lbcgo.examples']

package_data = \
{'': ['*'], 'lbcgo': ['conf/*']}

install_requires = \
['astropy==0', 'ccdproc>=2.2.0,<3.0.0', 'numpy>=1.21.0,<2.0.0']

setup_kwargs = {
    'name': 'lbcgo',
    'version': '0.1.1',
    'description': "Data reduction for the LBT's Large Binocular Camera",
    'long_description': None,
    'author': 'Chris Howk',
    'author_email': 'jhowk@nd.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
