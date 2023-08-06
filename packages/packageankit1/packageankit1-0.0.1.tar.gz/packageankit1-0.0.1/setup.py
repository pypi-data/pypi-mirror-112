from setuptools import setup, find_packages
#import codecs
#import os

VERSION = '0.0.1'
DESCRIPTION = 'ANOVA Python'
LONG_DESCRIPTION = 'A package to find the ANOVA for a CSV file.'

# Setting up
setup(
    name="packageankit1",
    version=VERSION,
    author="Ankit Tiwari",
    author_email="ankittiwari123321@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas','numpy'],
    keywords=['python', 'ANOVA', 'SSB', 'SSW', 'Ankit Tiwari'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)