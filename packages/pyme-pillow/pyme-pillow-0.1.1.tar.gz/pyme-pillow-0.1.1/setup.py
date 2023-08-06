# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyme']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.2.0,<9.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pyme-pillow',
    'version': '0.1.1',
    'description': 'A Pillow based image editing package optimized for the creation of memes',
    'long_description': '# Pyme\nA Pillow based image editing package optimized for the creation of memes',
    'author': 'Spookdot',
    'author_email': '55836077+Spookdot@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
