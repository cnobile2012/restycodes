import os, sys

__version__ = "0.1.0"

from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='RestyCodes',
      version=__version__,
      description="A Python implementation of the HTTP response codes.",
      long_description=read('README.md'),
      keywords="HTTP status python",
      author='Carl J. Nobile',
      author_email='carl.nobile@gmail.com',
      maintainer='Carl J. Nobile',
      maintainer_email='carl.nobile@gmail.com',
      url='https://github.com/cnobile2012/restycodes',
      license='',
      classifiers=[
          "Intended Audience :: Developers",
          "License :: OSI Approved",
          "Natural Language :: English",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules :: HTTP",
          ],
      download_url="https://github.com/cnobile2012/restycodes/archive/master.zip",
      platforms=["Linux", "UNIX", "Windows", "MacOS"],
      py_modules=['rulesengine.__init__', 'rulesengine.rules_engine',
                  'restycodes.__init__', 'restycodes.resty_codes'],
      #data_files=[('restycodes/tests',
      #             ['test/ll_test.py',],),
      #           ],
      zip_safe=True
      )
