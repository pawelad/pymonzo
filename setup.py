# -*- coding: utf-8 -*-
from __future__ import print_function

from setuptools import setup, find_packages


# Convert description from markdown to reStructuredText
try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst', 'markdown')
except (IOError, ImportError):
    description = ''


setup(
    name='pymonzo',
    url='https://github.com/pawelad/pymonzo',
    download_url='https://github.com/pawelad/pymonzo/releases/latest',
    bugtrack_url='https://github.com/pawelad/pymonzo/issues',
    version='0.1.0',
    license='MIT License',
    author='Paweł Adamczak',
    author_email='pawel.ad@gmail.com',
    maintainer='Paweł Adamczak',
    maintainer_email='pawel.ad@gmail.com',
    description='Python wrapper for Mondo public API',
    long_description=description,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests>=2.11.1',
        'six>=1.10.0',
    ],
    extras_require={
        'testing': ['pytest'],
    },
    keywords='icon font export font awesome octicons',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
