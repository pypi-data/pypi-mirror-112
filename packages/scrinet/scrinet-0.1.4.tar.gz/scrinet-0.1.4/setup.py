#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

import codecs
import os.path

# https://stackoverflow.com/questions/26900328/install-dependencies-from-setup-py
import os
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
#install_requires = []  # Examples: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
   with open(requirementPath) as f:
       install_requires = f.read().splitlines()


# versioning handled by the first method on:
# https://packaging.python.org/guides/single-sourcing-package-version/
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(name='scrinet',
      version=get_version("scrinet/__init__.py"),
      description='Modelling',
      author='Sebastian Khan, Rhys Green',
      author_email='khans22@cardiff.ac.uk, greenr10@cardiff.ac.uk',
      packages=find_packages(),
      #install_requires=install_requires,
      url='https://gitlab.com/SpaceTimeKhantinuum/scrinet',
      scripts=[
          'bin/pipeline/scrinet_build_rb',
          'bin/pipeline/scrinet_evaluate_model',
          'bin/pipeline/scrinet_evaluate_coprec_model',
          'bin/pipeline/scrinet_evaluate_7d_coprec_model',
          'bin/pipeline/scrinet_gen_ts_data',
          'bin/pipeline/scrinet_gen_wf_data_3d_non_prec',
          'bin/pipeline/scrinet_combine_wf_data',
          'bin/pipeline/scrinet_fit',
          'bin/pipeline/scrinet_gen_wf_data_2d_non_prec',
          'bin/pipeline/scrinet_gen_wf_data_non_spinning',
          'bin/pipeline/scrinet_gen_wf_data_3d_prec_single_spin',
          'bin/pipeline/scrinet_gen_wf_data_3d_prec_single_spin_coprec',
          'bin/pipeline/scrinet_gen_wf_data_7d_prec_single_spin_coprec',
          'bin/pipeline/scrinet_representation_error',
          'bin/pipeline/scrinet_make_workflow',
          'bin/pipeline/scrinet_make_webpage'
      ]
      )
