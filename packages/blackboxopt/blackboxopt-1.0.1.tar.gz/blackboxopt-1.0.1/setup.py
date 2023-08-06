# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blackboxopt',
 'blackboxopt.examples',
 'blackboxopt.optimization_loops',
 'blackboxopt.optimizers',
 'blackboxopt.optimizers.staged',
 'blackboxopt.visualizations']

package_data = \
{'': ['*']}

install_requires = \
['parameterspace>=0.7.2,<0.8.0']

extras_require = \
{'all': ['numpy>=1.20.1,<2.0.0',
         'plotly>=4.14.3,<5.0.0',
         'scipy>=1.6.0,<2.0.0',
         'statsmodels>=0.12.2,<0.13.0',
         'dask>=2021.2.0,<2022.0.0',
         'distributed>=2021.2.0,<2022.0.0',
         'pandas>=1.2.4,<2.0.0'],
 'bohb': ['numpy>=1.20.1,<2.0.0',
          'scipy>=1.6.0,<2.0.0',
          'statsmodels>=0.12.2,<0.13.0'],
 'dask': ['dask>=2021.2.0,<2022.0.0', 'distributed>=2021.2.0,<2022.0.0'],
 'hyperband': ['numpy>=1.20.1,<2.0.0'],
 'testing': ['numpy>=1.20.1,<2.0.0'],
 'visualization': ['plotly>=4.14.3,<5.0.0',
                   'scipy>=1.6.0,<2.0.0',
                   'pandas>=1.2.4,<2.0.0']}

setup_kwargs = {
    'name': 'blackboxopt',
    'version': '1.0.1',
    'description': 'A common interface for blackbox optimization algorithms along with useful helpers like parallel optimization loops, analysis and visualization scripts.',
    'long_description': None,
    'author': 'Bosch Center for AI, Robert Bosch GmbH',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
