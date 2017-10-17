#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # No requirements only standard lib modules
]

setup(
    name='pymoney',
    version='0.1.2',
    description=("Implementation of the Money pattern from Patterns of"
                 " enterprise application architecture by Martin Fowler"),
    long_description=readme + '\n\n' + history,
    author="Holger Rother",
    author_email='hrother@hrother.org',
    url='https://github.com/hrother/pymoney',
    packages=[
        'pymoney',
    ],
    package_dir={'pymoney':
                 'pymoney'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pymoney',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
