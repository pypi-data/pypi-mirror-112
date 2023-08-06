# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wallstreet']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.5,<5.0', 'requests>=2.12,<3.0', 'scipy>=1.5,<2.0']

setup_kwargs = {
    'name': 'wallstreet',
    'version': '0.3.1',
    'description': 'Stock and Option tools',
    'long_description': None,
    'author': 'Mike Dallas',
    'author_email': 'mcdallas@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
