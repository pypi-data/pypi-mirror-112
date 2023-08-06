from setuptools import setup, find_packages
import codecs
import os



VERSION = '0.0.15'
DESCRIPTION = 'a python package to benchmarks algorithms against various datasets'

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Setting up
setup(
    name="base2lines",
    version=VERSION,
    author="Vishwas",
    author_email="vishwasgoyal47@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["seaborn","scikit-learn","xgboost"],
    keywords=[],
    long_description=long_description,
    long_description_content_type='text/markdown',
    # package_dir={'':'baseline'},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)