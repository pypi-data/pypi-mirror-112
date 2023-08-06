#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import find_packages
import sys
if sys.version_info < (2, 5):
    sys.exit('Python 2.5 or greater is required.')
 
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
 
 
with open('README.rst', 'rb') as fp:
    readme = fp.read()
 
VERSION = "1.0.5"

LICENSE = "MIT"

 
setup(
    include_package_data=True,
    name='skilltree',
    version=VERSION,
    description=(
        'skills for material physics'
    ),
    long_description=readme,
    author='BrienZhang',
    author_email='brienzhang@sina.com',
    maintainer='Brien',
    maintainer_email='',
    license=LICENSE,
    packages=find_packages(),
    platforms=["all"],
    url='',
    install_requires=[  
        "pygame" 
        ],  
    classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
)
