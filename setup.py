#!/usr/bin/env python
# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
import mining


REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()
                if not i.startswith("http")]

dependency_links = [i.strip() for i in open("requirements.txt").readlines()
                    if i.startswith("http")]

classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Web Environment",
    'Framework :: Bottle',
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: JavaScript",
    "Programming Language :: Python :: 2.7",
    'Programming Language :: Python',
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Scientific/Engineering :: Information Analysis'
]

try:
    long_description = open('README.md').read()
except:
    long_description = mining.__description__

setup(name='mining',
      version=mining.__version__,
      description=mining.__description__,
      long_description=long_description,
      classifiers=classifiers,
      keywords='open mining bi business intelligence platform riak',
      author=mining.__author__,
      author_email=mining.__email__,
      url='http://openmining.io',
      download_url="https://github.com/avelino/mining/tarball/master",
      license=mining.__license__,
      packages=find_packages(exclude=('doc', 'docs',)),
      install_requires=REQUIREMENTS,
      dependency_links=dependency_links,
      test_suite='nose.main',
      include_package_data=True,
      zip_safe=False)
