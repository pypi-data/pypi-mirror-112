# -*- coding: UTF-8 -*-
import os

def readme():
    with open("README.md") as f:
        return f.read()

from setuptools import setup 
setup(
    name='promoterExtract',
    version='0.2',
    keywords='promoter',
    description='Extract promoter sequence for biologists',
    long_description_content_type='str',
    long_description=readme(),
    author='zhusitao',
    author_email='zhusitao1990@163.com',
    url='https://github.com/zhusitao1990',
    include_package_data=True,
    packages=['promoterExtract'],
    license='MIT',
    install_requires = ['requests'])
