# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['staliro', 'staliro.optimizers', 'staliro.parser']

package_data = \
{'': ['*'], 'staliro.parser': ['grammar/*']}

install_requires = \
['antlr4-python3-runtime>=4.5.3,<4.6.0',
 'attrs>=21.0.0,<22.0.0',
 'numpy>=1.20.2,<2.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'scipy>=1.6.2,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.7.4,<4.0.0'],
 'docs': ['Sphinx>=3.5.3,<4.0.0', 'sphinx-autodocgen>=1.2,<2.0'],
 'tests': ['pandas>=1.2.3,<2.0.0'],
 'tltk': ['tltk-mtl>=0.0.27,<0.0.28']}

setup_kwargs = {
    'name': 'psy-taliro',
    'version': '1.0.0a11',
    'description': 'System-level verification library using STL',
    'long_description': None,
    'author': 'Quinn Thibeault',
    'author_email': 'qthibeau@asu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
