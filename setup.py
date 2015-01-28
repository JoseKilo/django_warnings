#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='django-warnings',
    version='1.0.0',
    author='rockabox',
    author_email='tech@rockabox.com',
    packages=['django_warnings'],
    url='https://github.com/rockabox/django_warnings',
    license='MIT',
    description='Dynamic warnings with your Django models',
    classifiers=[
        'Development Status :: 2 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'Django>=1.7',
    ],
)
