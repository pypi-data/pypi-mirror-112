# coding: utf-8
from setuptools import setup, find_packages
from setuptools.extension import Extension
from distutils.extension import Extension
from codecs import open
from os import path
import glob
import re
import sys

from bamr import __version__ as bamr_version
here = path.abspath(path.dirname("__file__"))

name="bamr"
version = bamr_version

if sys.version_info.major != 3:
	raise EnvironmentError(f"{name} is a python module that requires python3, and is not compatible with python2.")

setup(
	name=name,
	version=version,
	description="bamr is a lightweight python library for reading bam files",
	url="https://github.com/cschu/bamr",
	author="Christian Schudoma",
	author_email="cschu1981@gmail.com",
	license="MIT",
	download_url="https://github.com/cschu/bamr/archive/refs/tags/v0.1.1.tar.gz",
	classifiers=[
		"Development Status :: 4 - Beta",
		"Topic :: Scientific/Engineering :: Bio-Informatics",
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX :: Linux",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9"
	],
	zip_safe=False,
	keywords="bam reading light-weight library",
	packages=find_packages(exclude=["test"]),
	install_requires=[],
	package_data={},
	include_package_data=True,
	data_files=[],
)
