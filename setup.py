#!/usr/bin/env python

from distutils.core import setup

setup(
    name='OMFTools',
    version='0.1',
    description='Tools for modifying OMF2097 files',
    author='Tuomas Virtanen',
    author_email='katajakasa@gmail.com',
    url='https://github.com/omf2097/pyomftools',
    packages=['omftools', 'omftools.pyshadowdive'],
    license='MIT'
)