#!/usr/bin/env python

from setuptools import setup, find_packages
from dyncss import __version__ as version
from dyncss import __doc__ as doc

import os


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        with open(filepath, 'r') as fh:
            return fh.read()
    except IOError:
        return ''


setup(
    name='django-dyncss',
    version=version,
    author='Julien Colot',
    author_email='julien.colot@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/jcolot/django-dyncss',
    license='MIT',
    description=' '.join(doc.splitlines()).strip(),
    install_requires=read_file('requirements.txt').splitlines(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'Framework :: Django :: 2.2',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    long_description=read_file('README.rst'),
    long_description_content_type='text/x-rst',
)
