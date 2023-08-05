#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='paropy',
      version='0.0.5', 
      description='Python package to process data from PARODY-JA4.3 dynamo simulations.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/jnywong/paropy',
      author='Jenny Wong',
      author_email='jenny.wong@univ-grenoble-alpes.fr',
      license='MIT',
      packages=['paropy'],
      package_data={'paropy': ['scripts/*.py', 'data/CHAOS-7.7.mat']},
      setup_requires=["numpy"],
      install_requires=['pytest','pandas','matplotlib','scipy','proj','pyshp','geos','shapely','cartopy','h5py','chaosmagpy'],
      )
