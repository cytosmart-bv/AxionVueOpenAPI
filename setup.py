"""The setup script."""

from setuptools import setup, find_packages

with open("README.md", errors="ignore") as readme_file:
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
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Bio-Informatics ",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
    description="This is a python wrapper for the Axion Vue windows app to use it headless",
    entry_points={"console_scripts": ["AxionVueOpenAPI=AxionVueOpenAPI.cli:__init__"]},
    install_requires=requirements,
    long_description=readme + "\n\n" + history + "\n\n" + license,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="AxionVueOpenAPI",
    name="AxionVueOpenAPI",
    packages=find_packages(include=["AxionVueOpenAPI*"], exclude=["docs*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/cytosmart-bv/AxionVueOpenAPI",
    version="1.3.1b1",
    zip_safe=False,
)
