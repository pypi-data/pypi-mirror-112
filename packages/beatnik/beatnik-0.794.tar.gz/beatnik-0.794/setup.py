from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'beatnik',
  version = '0.794',
  license='MIT',
  description = 'beatnik interpreter',
  long_description=long_description,
  long_description_content_type='text/markdown',
  packages=find_packages(),
  author = 'Experimental Informatics',
  author_email = 't.liu@khm.de',
  url = 'https://github.com/experimental-informatics/beatnik',
  keywords = ['beatnik', 'esoteric programming language', 'stack-based'],
  install_requires=[
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
