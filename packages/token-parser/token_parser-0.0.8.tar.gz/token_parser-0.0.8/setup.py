# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

VERSION = '0.0.8'
DESCRIPTION = 'String token parser'
LONG_DESCRIPTION = here.joinpath("token_parser").joinpath("readme.md").read_text(encoding='utf-8')

# Setting up
setup(
    name="token_parser",
    version=VERSION,
    author="Breno RdV",
    author_email="hello@raccoon.ninja",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["parameterized", "pytz", "python-dateutil"],
    keywords=['python', 'token', 'parser', 'test'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux"
    ]
)