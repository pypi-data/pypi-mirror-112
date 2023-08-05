# -*- coding: UTF-8 -*-
import os

def readme():
    with open("README.rst") as f:
        return f.read()

from setuptools import setup 
setup(
    name='promoterExtract',
    version='0.7',
    keywords='promoter',
    description='Extract promoter sequence for biologists',
    long_description_content_type='text/markdown',
    long_description=readme(),
    entry_points = {'console_scripts': ['get_promoter=promoterExtract.command_line:main']},
    author='zhusitao',
    author_email='zhusitao1990@163.com',
    url='https://github.com/zhusitao1990',
    include_package_data=True,
    packages=['promoterExtract'],
    license='MIT',
    install_requires = ['requests'])
