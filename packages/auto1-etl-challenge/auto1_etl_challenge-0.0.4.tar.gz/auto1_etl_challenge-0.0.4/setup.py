from setuptools import setup, find_packages
from os import path

VERSION = '0.0.4'
description = 'Auto1 ETL Challenge'


with open(path.join(r'C:\Users\muhammad.aqib\Desktop\auto1', 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


# Setting up
setup(
    name="auto1_etl_challenge",
    version=VERSION,
    author="Muhammad Aqib",
    author_email="<inbox.aqib@gmail.com>",
    description=description,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['auto1', 'challenge_me', 'etl pipeline',],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)