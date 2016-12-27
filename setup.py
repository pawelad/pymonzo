# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import io
import os
import re

from setuptools import setup, find_packages


# Convert description from markdown to reStructuredText
try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst', 'markdown')
except (OSError, ImportError):
    description = ''


# Get package version number
# Source: https://packaging.python.org/single_source_version/
def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='pymonzo',
    url='https://github.com/pawelad/pymonzo',
    download_url='https://github.com/pawelad/pymonzo/releases/latest',
    bugtrack_url='https://github.com/pawelad/pymonzo/issues',
    version=find_version('pymonzo', '__init__.py'),
    license='MIT License',
    author='Paweł Adamczak',
    author_email='pawel.ad@gmail.com',
    maintainer='Paweł Adamczak',
    maintainer_email='pawel.ad@gmail.com',
    description='An - dare I say it - awesome Python library that smartly '
                'wraps Monzo public API and allows you to use it directly in '
                'your Python project.',
    long_description=description,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'python-dateutil>=2.6.0',
        'requests>=2.12.4',
        'requests-oauthlib>=0.7.0',
        'six>=1.10.0',
    ],
    extras_require={
        'testing': ['pytest'],
    },
    keywords='monzo api',
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
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
