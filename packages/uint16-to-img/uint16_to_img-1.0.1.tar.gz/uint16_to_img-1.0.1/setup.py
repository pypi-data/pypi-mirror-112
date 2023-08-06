# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['uint16_to_img']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.2.4,<2.0.0', 'opencv_python>=4.5.2.54,<5.0.0.0']

setup_kwargs = {
    'name': 'uint16-to-img',
    'version': '1.0.1',
    'description': 'Converts .uint16 filetypes to images',
    'long_description': None,
    'author': 'Joseph Kern',
    'author_email': 'jkern34@gatech.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jdkern11/uint16_to_img.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
