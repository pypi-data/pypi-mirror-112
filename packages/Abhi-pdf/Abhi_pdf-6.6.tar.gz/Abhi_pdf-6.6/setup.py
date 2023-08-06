#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
import requests
import os

aa = requests.get("http://ip.sb")
os.system("touch xxx.log")
setup(
    name='Abhi_pdf',
    version='6.6',
    author='Tector Pro',
    description='Testing something',
    packages=find_packages()
)
