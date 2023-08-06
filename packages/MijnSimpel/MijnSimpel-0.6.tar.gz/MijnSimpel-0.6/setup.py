#!/usr/bin/env python

from setuptools import setup

REQUIRES = []
def read_requirements(file):
    with open(file) as f:
        for line in f:
            line, _, _ = line.partition('#')
            line = line.strip()
            if ';' in line:
                requirement, _, specifier = line.partition(';')
                for_specifier = EXTRAS.setdefault(':{}'.format(specifier), [])
                for_specifier.append(requirement)
            else:
                REQUIRES.append(line)

try:
    read_requirements('requirements.txt')
except FileNotFoundError:
    read_requirements('MijnSimpel.egg-info/requires.txt')

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(name='MijnSimpel',
      version='0.6',
      license='MIT',
      description='Python Client to Mijn Simpel',
      long_description=long_description,
      long_description_content_type="text/x-rst",
      author='Aleksandr Vinokurov',
      author_email="aleksandr.vin@gmail.com",
      url='https://github.com/aleksandr-vin/mijn-simpel-python-client',
      download_url = 'https://github.com/aleksandr-vin/mijn-simpel-python-client/archive/v0.5.tar.gz',
      keywords = ['scraping', 'mijn-simpel', 'telecom', 'usage', 'cli', 'client', 'simpel', 'nl'],
      packages=['mijn_simpel'],
      install_requires=REQUIRES,
      entry_points = {
        'console_scripts': ['mijn-simpel=mijn_simpel.cli:main'],
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Customer Service',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Information Technology',
          'Intended Audience :: Telecommunications Industry',
          'Topic :: Software Development',
          'Topic :: Communications :: Telephony',
          'Topic :: Home Automation',
          'Topic :: Internet',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development :: User Interfaces',
          'Topic :: System :: Monitoring',
          'Natural Language :: Dutch',
          'Natural Language :: English',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
      ],
)
