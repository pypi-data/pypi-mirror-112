#!/usr/bin/env python
from setuptools import setup, find_packages
setup(
 name = 'lujxdemo',
 version = '0.0.3',
 description = 'library ',
 long_description = 'library ',
 author = 'Lujx',
 author_email = '20920139@qq.com',
 url = 'http://10.177.132.101',
 license = 'MIT Licence',
 keywords = 'testing testautomation',
 platforms = 'any',
 python_requires = '>=3.6.*',
 install_requires = [],
 package_dir = {'': 'src'},
 packages = find_packages('src')
 )


