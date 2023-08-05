#!/usr/bin/env python

from setuptools import setup


def read_content(filepath):
    with open(filepath, 'r') as f:
        return f.read()


classifiers = ['Development Status :: 4 - Beta',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: Home Automation',
               'Topic :: System :: Hardware']

setup(
    name                          = 'rpi_gpio_devices',
    version                       = '0.1.2',
    author                        = 'Daniel Todor',
    description                   = 'This module provides device classes for controlling the gpio ports',
    long_description              = read_content('README.md'),
    long_description_content_type = 'text/markdown',
    license                       = 'MIT',
    keywords                      = ['Raspberry', 'Pi', 'GPIO'],
    url                           = 'https://github.com/danieltodor/rpi-gpio-devices',
    classifiers                   = classifiers,
    packages                      = ['rpi_gpio_devices'],
    package_dir                   = {'rpi_gpio_devices': 'src'},
    install_requires              = ['RPi.GPIO==0.7.1a4']
)
