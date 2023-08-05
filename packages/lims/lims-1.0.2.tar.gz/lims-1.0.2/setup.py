#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import os
import json
from setuptools import setup, find_packages

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

version_info = json.load(open(os.path.join(BASE_DIR, 'lims', 'version.json')))


setup(
    name=version_info['prog'],
    version=version_info['version'],
    author='suqingdong',
    author_email='suqingdong@novogene.com',
    description='toolkits for lims',
    long_description=open(os.path.join(BASE_DIR, 'README.md')).read(),
    long_description_content_type="text/markdown",
    url='https://github.com/suqingdong/lims',
    license='BSD License',
    install_requires=open(os.path.join(BASE_DIR, 'requirements.txt')).read().split('\n'),
    packages=find_packages(),
    include_package_data=True,
    # scripts=['lims/bin/lims-main.py'],
    entry_points={'console_scripts': [
        'lims = lims.bin.main:main',
    ]},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
)
