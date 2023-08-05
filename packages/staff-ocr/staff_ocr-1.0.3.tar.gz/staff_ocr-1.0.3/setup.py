# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['staff_ocr',
 'staff_ocr.angnet',
 'staff_ocr.crnn',
 'staff_ocr.dbnet',
 'staff_ocr.util']

package_data = \
{'': ['*']}

install_requires = \
['hanlp-downloader>=0.0.22,<0.1.0',
 'loguru>=0.5.3,<0.6.0',
 'numpy>=1.19.5,<2.0.0',
 'onnxruntime>=1.8.0,<1.9.0',
 'opencv-python>=4.5.2,<4.6.0',
 'pillow>=8.2.0,<8.3.0',
 'pyclipper>=1.2.1,<2.0.0',
 'shapely>=1.7.1,<2.0.0',
 'termcolor>=1.1.0,<1.2.0']

setup_kwargs = {
    'name': 'staff-ocr',
    'version': '1.0.3',
    'description': '',
    'long_description': None,
    'author': 'JimZhang',
    'author_email': 'zzl22100048@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
