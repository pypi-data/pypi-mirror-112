#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from os.path import join, dirname
from setuptools import setup


def get_version(package):
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    return [dirpath for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


setup(
    name='Sanic-thumbnails',
    version=get_version('sanic_thumbnails'),
    url='https://github.com/q8977452/sanic-thumbnails',
    license='MIT',
    author='Ray Sin',
    author_email='ray0101.sin@gmail.com',
    description='A simple extension to create a thumbs for the Sanic',
    py_modules=['Sanic_thumbnails'],
    packages=get_packages('sanic_thumbnails'),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[],

    test_suite='tests',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
    ]
)
