#!/usr/bin/env python

from setuptools import setup, find_packages

with open("requirements.txt", "r") as reqs_file:
    requirements = reqs_file.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = '0.2.7'

setup(name='radon-defect-predictor',
      version=VERSION,
      description='A Python library to train machine learning models for defect prediction of infrastructure code.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Stefano Dalla Palma',
      maintainer='Stefano Dalla Palma',
      author_email='stefano.dallapalma0@gmail.com',
      url='https://github.com/radon-h2020/radon-defect-predictor',
      download_url='https://github.com/radon-h2020/radon-defect-predictor/archive/{0}.tar.gz'.format(VERSION),
      packages=find_packages(exclude=('tests',)),
      entry_points={
          'console_scripts': ['radon-defect-predictor=radondp.cli:main'],
      },
      python_requires='>=3.6',
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "License :: OSI Approved :: Apache Software License",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Operating System :: OS Independent"
      ],
      install_requires=requirements
)
