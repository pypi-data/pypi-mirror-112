# -*- coding: utf-8 -*-

import sys

from setuptools import find_packages, setup

if sys.version_info < (3, 6):
    raise RuntimeError("ddf_conversions 1.x requires Python 3.6+")

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="ddf_conversions",
    version="1.0",
    description="ddf转换工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ddf118",
    author_email="dyf402@163.com",
    packages=find_packages(),
    url="https://github.com/ddf118/ddf.conversions",
    python_requires=">=3.6",
    install_requires=required,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
