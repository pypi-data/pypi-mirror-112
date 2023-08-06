# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polliwog',
 'polliwog._common',
 'polliwog.box',
 'polliwog.line',
 'polliwog.plane',
 'polliwog.pointcloud',
 'polliwog.polyline',
 'polliwog.segment',
 'polliwog.shapes',
 'polliwog.transform',
 'polliwog.tri']

package_data = \
{'': ['*']}

install_requires = \
['numpy<1.19.0', 'ounce>=1.1.0,<2.0', 'vg>=1.11.1']

setup_kwargs = {
    'name': 'polliwog',
    'version': '1.0.0b14',
    'description': '2D and 3D computational geometry library',
    'long_description': None,
    'author': 'Paul Melnikow',
    'author_email': 'github@paulmelnikow.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://polliwog.dev/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
