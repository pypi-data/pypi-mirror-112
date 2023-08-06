# -*- encoding: UTF-8 -*-
from setuptools import setup, find_packages

VERSION = '0.1.5'

setup(name='cctxpa',
      version=VERSION,
      description="A command line tool for CCTX to analyser pcap and compare with CCTX's observables",
      long_description='',
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python cctx pcap cctxpa terminal',
      author='zoeyyy',
      author_email='yzou10@uoguelph.ca',
      url='https://github.com/zoeyyyzou/cctx-pcap-analyser',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'dpkt',
          'progress',
          'requests'
      ],
      entry_points={
          'console_scripts': [
              'cctxpa = cctxpa.cctxpa:main'
          ]
      },
      )
