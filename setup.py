
from setuptools import setup, find_packages

setup(
    name='pyhome',
    version='0.1.1',
    description='Dotfile management and synchronisation tool',
    long_description=open('README.rst').read(),
    url='https://github.com/acroz/pyhome',
    author='Andrew Crozier',
    author_email='wacrozier@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
          'pyhome=pyhome.__main__:main'
        ]
    }
)
