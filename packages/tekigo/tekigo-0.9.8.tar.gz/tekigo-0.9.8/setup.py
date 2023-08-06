#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from glob import glob
from os.path import basename, splitext
from setuptools import setup, find_packages
import os.path as path


this_directory = path.abspath(path.dirname(__file__))
with open('README.md', 'r') as f:
    readme = f.read()

with open(path.join(this_directory, 'VERSION'), encoding='utf-8') as f:
    version = f.read()

with open('LICENSE.txt') as f:
     license = f.read()

setup(
    name='tekigo',
    version=version,
    description='Cerfacs mesh adaption toolkit',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='CoopTeam-CERFACS',
    author_email='coop@cerfacs.fr',
    url='https://gitlab.com/cerfacs/tekigo',
    license ="MIT License",
    license_files = license,
    keywords=["tekigo API"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob('src/**.py')],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    include_package_data=True,
    install_requires=[
        'numpy',
        'scipy',
        'PyYAML',
        'hdfdict>=0.3.1,<1.0',
        'nob',
        'h5py',
        'arnica']
)
