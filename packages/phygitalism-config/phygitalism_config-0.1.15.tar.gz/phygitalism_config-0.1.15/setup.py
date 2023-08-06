# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['phygitalism_config', 'phygitalism_config.special_types']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'typing-inspect>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['generate-config = phygitalism_config.__main__:main']}

setup_kwargs = {
    'name': 'phygitalism-config',
    'version': '0.1.15',
    'description': '',
    'long_description': None,
    'author': 'Phygitalism',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
