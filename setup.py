#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

with open("LICENSE") as license_file:
    license = license_file.read()

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.read().split("\n")

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest", "pillow"]

setup(
    author="Tom Nijhof",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only ",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Bio-Informatics ",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
    description="This is a python wrapper around the Lux Client windows solution",
    entry_points={"console_scripts": ["luxconnector=luxconnector.cli:__init__"]},
    install_requires=requirements,
    long_description=readme + "\n\n" + history + "\n\n" + license,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="luxconnector",
    name="luxconnector",
    packages=find_packages(include=["luxconnector*"], exclude=["docs*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/cytosmart-bv/luxconnector",
    version="1.0.4",
    zip_safe=False,
)
