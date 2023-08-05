
#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys
 
setup(
    name="pytest-tmreport",
    version="1.0.1",
    author="Kevin Kai",
    author_email="zykzml7788@sina.com",
    description="this is a vue-element ui report for pytest",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/desion/tidy_page",
    packages=['pytest-tmreport'],
    install_requires=[
        "pytest"
        ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
