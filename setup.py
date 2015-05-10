#!/usr/bin/env python
# coding: utf-8


from setuptools import setup
import os
import re

py_modules = []
for fname in os.listdir('/home/ilya/opt/programming/fablib'):
    m = re.match("(.*)\.py$", fname)
    if m:
        py_modules.append(m.group(1))
        
setup(
    name = "fablib",
    version = 1,    

    #py_modules = py_modules,
)