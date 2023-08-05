#!/usr/bin/env python

import os

from setuptools import setup, find_packages
from ois.sdk import __version__

ROOT = os.path.dirname(__file__)

requires = ['requests', 'PyYAML']

setup(
    name='ois-sdk',
    version=__version__,
    description='The official OIS SDK for the Python programming language.',
    long_description=open('README.md', 'rb').read().decode('utf-8'),
    long_description_content_type='text/markdown',
    author='shanhe SDK Group',
    url='https://github.com/shanhe-nsccjn/ois-sdk-python',
    author_email='sdk_group@shanhe.com',
    scripts=[],
    packages=find_packages('.', exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    namespace_packages=['ois'],
    package_dir={'sdk': 'ois'},
    include_package_data=True,
    install_requires=requires,
    license="Apache License 2.0",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ], )
