# -*- coding: utf-8 -*-
from enviopack import __version__ as VERSION, __author__ as AUTHOR
from setuptools import setup, find_packages

setup(
  name="enviopack",
  version=VERSION,
  url="https://github.com/fedegobea/enviopack",
  author=AUTHOR,
  author_email="gitfgobea@gmail.com",
  description="Integration Helper with enviopack",
  long_description=open('README.md').read(),
  packages=find_packages(),
  install_requires=['requests'],
  classifiers=[
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.7',
  ],
)