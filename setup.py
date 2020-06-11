#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Numpy>=1, <2",
    "opencv-python>=4.1, <5",
    "websocket>=0.2.1, <0.3",
    "websocket-client>=0.57.0, <0.58",
]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest", "pillow"]

setup(
    author="Tom Nijhof",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="This is a python wrapper around the Lux Client windows solution",
    entry_points={"console_scripts": ["luxconnector=luxconnector.cli:__init__"]},
    install_requires=requirements,
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="luxconnector",
    name="luxconnector",
    packages=find_packages(include=["luxconnector*"], exclude=["docs*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://cytosmart.com",
    version="0.1.1",
    zip_safe=False,
)
