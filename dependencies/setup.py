# -*- coding: utf-8 -*-
"""
@author: chengmarc
@github: https://github.com/chengmarc

"""
from setuptools import setup, find_packages

setup(
    name='cmcs-dependencies',
    version='1.0',
    packages=find_packages(),
    install_requires=['tk==0.1.0', 'requests==2.28.2', 'pandas==2.1.0']
)