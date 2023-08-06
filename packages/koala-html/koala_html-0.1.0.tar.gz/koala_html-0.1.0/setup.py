#!/usr/bin/env python

from setuptools import setup
import os

import versioneer


def get_long_description():
    """ Finds the README and reads in the description """
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'README.rst')) as f:
        long_description = f.read()
    return long_description


long_description = get_long_description()

setup(name='koala_html',
      description='A simple HTML page generator',
      long_description=long_description,
      url='https://github.com/GregoryAshton/koala_html',
      author='Greg Ashton',
      author_email='gregory.ashton@ligo.org',
      license="MIT",
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      packages=['koala_html'],
      package_dir={'koala_html': 'src'},
      package_data={'koala_html': ["simple_style.css"]},
      entry_points={'console_scripts':
                    ['koala_table=koala_html.table:main']
                    },
      classifiers=[
          "Programming Language :: Python :: 3.7",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent"])
