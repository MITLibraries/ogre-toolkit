# -*- coding: utf-8 -*-
import io
from setuptools import setup, find_packages

with io.open('README.rst') as f:
    readme = f.read()

with io.open('LICENSE') as f:
    license = f.read()

setup(
    name='Ogre-Toolkit',
    version='0.2.0',
    description='Work with OpenGeoMetadata repositories',
    long_description=readme,
    url='https://github.com/MITLibraries/ogre-toolkit.git',
    license=license,
    author='Mike Graves',
    author_email='mgraves@mit.edu',
    packages=find_packages(exclude=('docs', 'tests')),
    install_requires=['arrow', 'GitPython', 'six'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
