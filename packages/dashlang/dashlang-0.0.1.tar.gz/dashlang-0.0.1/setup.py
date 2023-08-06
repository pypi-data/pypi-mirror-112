#!/usr/bin/env python
from setuptools import find_packages, setup

with open("README.md") as fp:
    long_description_text = fp.read()

setup(
    name="dashlang",
    version="0.0.1",
    license="Unlicense",
    url="https://gitlab.com/runemaster/dashlang",
    description="Experimental markup language for creating rich dashboards using Dash",
    long_description=long_description_text,
    long_description_content_type="text/markdown",
    author="Pedro Dias",
    author_email="pedrodias.miguel@gmail.com",
    maintainer="Pedro Dias",
    maintainer_email="pedrodias.miguel@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Dash",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries"
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=[
        "dash>1.20.0",
        "parsimonious==0.8.1",
    ],
)
