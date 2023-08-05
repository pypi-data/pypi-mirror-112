#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='django_mirror_map',
    version='0.0.8',
    author='shiyifan17',
    author_email='shiyifan17@163.com',
    url='https://github.com/shi1fan',
    description=u'查找某个属性的映射属性',
    packages=['django_mirror_map'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'attr2map=django_mirror_map:attr2map',
            'unix2yymmdd=django_mirror_map:unix2yymmdd',
            'unix2day=django_mirror_map:unix2day',
            'useattr=django_mirror_map:useattr',
        ]
    }
)