from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Auto1 ETL Challenge'
LONG_DESCRIPTION = 'A package that allows you to perform simple ETL operations'

# Setting up
setup(
    name="auto1_etl_challenge",
    version=VERSION,
    author="Muhammad Aqib",
    author_email="<inbox.aqib@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
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