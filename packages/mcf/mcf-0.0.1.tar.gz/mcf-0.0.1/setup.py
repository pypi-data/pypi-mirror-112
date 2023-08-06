from distutils.core import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
  name = 'mcf',
  packages = ['mcf'],
  version = '0.0.1',
  license='MIT',
  description = 'mcf is a powerful package to estimate heterogeneous treatment effects for multiple treatment models in a selection-on-observables setting',
  author = 'mlechner',
  author_email = 'michael.lechner@unisg.ch',
  url = 'https://github.com/MCFpy/mcf',
  keywords = ['causal machine learning, heterogeneous treatment effects, causal forests'],
  long_description = read('README.txt'),
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9'
  ],
  install_requires=[
   'numpy<=1.21.0',
   'pandas',
   'scipy',
   'ray',
   'numba',
   'scikit-learn',
   'psutil',
   'sympy']
)
