#!/usr/bin/env python3

import setuptools
import new_reader

with open("README.md", "r") as fh:
    readme = fh.read()

setuptools.setup(
    name="new_reader",
    version=new_reader.version(),
    author="Adrian",
    author_email="spam@iodisco.com",
    description="Read http(s), multicast, and udp streams like files",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/futzu/new_reader",
    packages=setuptools.find_packages(),
    install_requires=[
      ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    python_requires=">=3.6",
)
