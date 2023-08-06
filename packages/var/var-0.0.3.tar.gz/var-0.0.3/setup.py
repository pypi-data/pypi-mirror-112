# -*- coding: utf-8 -*-
"""
Setup of VaR Package
====================
*Created on 28.06.2021 by bari_is*

*For COPYING and LICENSE details, please refer to the LICENSE file*

"""
from setuptools import find_packages
from setuptools import setup


def get_packages():
    find_packages(exclude=['docs']),
    return find_packages()


# ------------------------------------------------------------------------------------------------------------
# Environmental Functions
# ------------------------------------------------------------------------------------------------------------
def get_version():
    """
    Function to get the version.

    Returns
    -------
    out : str
    """
    version = dict()
    with open("VaR/__version__.py") as fp:
        exec(fp.read(), version)

    return version['__version__']


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='var',

      version=get_version(),
      description='Different Methods to Estimate the Value-at-Risk of a portfolio.',
      packages=get_packages(),

      author="Ismail Baris",
      maintainer='Ismail Baris',

      url='https://github.com/ibaris/VaR',
      long_description='Different Methods to Estimate the Value-at-Risk of a portfolio.',

      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Intended Audience :: Science/Research',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: End Users/Desktop',
          'Programming Language :: Python :: 3.7',
          'Operating System :: Microsoft',

      ],
      include_package_data=True,
      )
