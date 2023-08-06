# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hyccup']

package_data = \
{'': ['*']}

install_requires = \
['hy==1.0a1']

setup_kwargs = {
    'name': 'hyccup',
    'version': '1.0.0a1.dev2',
    'description': 'A port of Clojure Hiccup for Hy',
    'long_description': None,
    'author': 'Guillaume Fayard',
    'author_email': 'guillaume.fayard@pycolore.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
