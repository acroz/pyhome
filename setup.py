
from setuptools import setup, find_packages

setup(name='pyhome',
      description='Dotfile management and synchronisation tool',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
            'pyhome=pyhome.__main__:main'
          ]
      })
