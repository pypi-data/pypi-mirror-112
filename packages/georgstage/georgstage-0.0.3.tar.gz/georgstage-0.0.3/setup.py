# coding=utf-8
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='georgstage',
    version='v0.0.3',
    download_url='https://github.com/skipperkongen/georgstage/archive/v0.0.3.tar.gz',
    licence='MIT',
    author="Pimin Konstantin Kefaloukos",
    author_email="skipperkongen@gmail.com",
    description="Hjælpeprogrammer til georgstage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skipperkongen/georgstage",
    packages=['georgstage'],
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
