#!/usr/bin/env python

from pathlib import Path

from setuptools import find_packages, setup

from congress_crawler import __version__


with (Path(__file__).parent / "requirements.txt").open() as f:
    required = f.read().splitlines()


setup(
    name="congress-crawler",
    version=__version__,
    author="Andrew Chen Wang",
    author_email="acwangpython@gmail.com",
    url="https://github.com/Hear-Ye/congress",
    description="Gathers data on the U.S. Congress.",
    long_description=open("README.md").read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP",
    ],
    license="CC0",
    packages=find_packages(),
    install_requires=required,
    include_package_data=True,
    zip_safe=False,
)
