#!/usr/bin/env python
import octohub
from distutils.core import setup

setup(
    name='octohub',
    version=octohub.__version__,
    description='Low level Python and CLI interface to GitHub',
    long_description=open('README.rst').read(),
    author='Alon Swartz',
    author_email='alon@turnkeylinux.org',
    url='https://github.com/turnkeylinux/octohub',
    license='GPLv3+',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
    packages=[
        'octohub',
    ],
)
