# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qvncwidget']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.4,<6.0.0',
 'Twisted>=21.2.0,<22.0.0',
 'pyDes>=2.0.1,<3.0.0',
 'service-identity>=21.1.0,<22.0.0']

setup_kwargs = {
    'name': 'qvncwidget',
    'version': '0.1.0',
    'description': 'Passive VNC QT Widget for Python using PyQt5',
    'long_description': '# pyQVNCWidget\nPassive VNC Widget for Python using PyQt5 \n',
    'author': 'zocker_160',
    'author_email': 'zocker1600@posteo.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zocker-160/pyQVNCWidget',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
