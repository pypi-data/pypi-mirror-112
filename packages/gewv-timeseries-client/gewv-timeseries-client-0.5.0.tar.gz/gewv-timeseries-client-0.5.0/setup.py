# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gewv_timeseries_client']

package_data = \
{'': ['*']}

install_requires = \
['influxdb-client>=1.16.0,<2.0.0',
 'loguru>=0.5.1,<0.6.0',
 'pandas>=1.2.4,<2.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'gewv-timeseries-client',
    'version': '0.5.0',
    'description': 'Client to read and write data from our timeseries db.',
    'long_description': None,
    'author': 'Karl',
    'author_email': 'karl_eugen.wolffgang@tu-dresden.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gewv-tu-dresden/timeseries-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
