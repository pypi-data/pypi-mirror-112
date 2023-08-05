#!/usr/bin/env python
from setuptools import find_packages, setup


project = "mend_circleci_python_library"
version = "0.2.0"


url = "https://github.com/jessemyers/mend-circleci-python-library"
long_description = f"See {url}"
try:
    with open("README.md") as file_:
        long_description = file_.read()
except IOError:
    pass


setup(
    name=project,
    version=version,
    license="MIT",
    description="Mend generator for CircleCI python libraries.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jesse Myers",
    url=url,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        "mend>=0.4.0",
    ],
    entry_points={
        "mend.generators": [
            "circleci-python-library = mend_circleci_python_library.generator:CircleCIGenerator",
        ],
    },
    extras_require=dict(
        dist=[
            "bumpversion>=0.6.0",
            "pip>=21.1.3",
            "setuptools>=57.1.0",
            "twine>=3.4.1",
            "wheel>=0.36.2",
        ],
        lint=[
            "flake8>=3.9.2",
            "flake8-isort>=4.0.0",
            "flake8-print>=4.0.0",
        ],
        test=[
            "pytest>=6.2.4",
        ],
        types=[
            "mypy>=0.910.0",
            "types-setuptools>=57.0.0",
        ],
    ),
)
