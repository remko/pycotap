#!/usr/bin/env python
# coding=utf-8

import os
from setuptools import setup, find_packages

def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
  name = "pycotap",
  version = "0.1.0",
  packages = find_packages(),
  # long_description = read('README.md'),

  # Metadata
  author = "Remko Tronçon",
  author_email = "dev@el-tramo.be",
  description = """A test runner that outputs TAP results to stdandard output.""",
  license = "MIT",
  keywords = "tap unittest testing",
  url = "https://el-tramo.be/pycotap",
  classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Utilities",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Testing"
  ],
)
