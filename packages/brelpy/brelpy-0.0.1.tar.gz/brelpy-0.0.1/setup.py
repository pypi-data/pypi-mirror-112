#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="brelpy",
    version="0.0.1",
    description="Module to connect to Brel-Home hubs.",
    long_description=long_description,
    license="GNU Affero General Public License v3",
    author="Rogier van der Geer",
    author_email="rogier@vander-geer.nl",
    url="https://gitlab.com/rogiervandergeer/brelpy",
    packages=find_packages(include=["brelpy"]),
    keywords=["brel", "smarthome", "blinds"],
    python_requires=">= 3.6",
    install_requires=["pycryptodome>=3.10.0"],
    extras_require={"test": ["pytest>=6.2.4", "pytest-mock>=3.6.1"]},
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Natural Language :: English",
        "Topic :: Home Automation",
    ],
)
