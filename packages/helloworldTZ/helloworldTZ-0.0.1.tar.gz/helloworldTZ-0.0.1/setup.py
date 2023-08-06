# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 19:45:54 2021

@author: jianzhezhen
"""

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
      name = "helloworldTZ",
      version = "0.0.1",
      description = "Say hello!",
      py_modules = {"helloworldTZ"},
      package_dir = {'': 'src'},
      classifiers = [
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          ],
      long_description = long_description,
      long_description_content_type = "text/markdown",
      install_requires = [
          "numpy",],
      extras_require = {
          "dev":[
              "pytest>=3.7",
              ],
          },
      url = "http://trevorzhen.com/" ,
      author = "trevorzhen",
      author_email = "trevorzhen@gmail.com",
      include_package_data = True,
      
      )