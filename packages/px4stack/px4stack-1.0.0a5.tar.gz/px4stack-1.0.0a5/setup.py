# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['px4stack']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.0.0,<22.0.0', 'docker>=5.0.0,<6.0.0']

setup_kwargs = {
    'name': 'px4stack',
    'version': '1.0.0a5',
    'description': '',
    'long_description': None,
    'author': 'Quinn Thibeault',
    'author_email': 'quinn.thibeault96@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
