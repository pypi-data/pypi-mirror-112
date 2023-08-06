from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.2'
DESCRIPTION = 'A COVID-19 web scrapping tool used to scrap data from the Worldometer website of US cases'

# Setting up
setup(
    name="covid-19-us-data",
    version=VERSION,
    author="Jimmy Tran",
    author_email="jimmytran1620@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['beautifulsoup4==4.9.1','bs4==0.0.1','requests'],
    keywords=['covid19', 'covid', 'web scraping', 'beautifulsoup'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

