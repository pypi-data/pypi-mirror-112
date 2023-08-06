#!/usr/bin/env python
from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = ['websockets>=9.1']

setup(
    name='tabby-connection-gateway',
    version='0.1.0',
    author="Eugene Pankov",
    author_email='e@ajenti.org',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    entry_points={
        'console_scripts': [
            'tabby_connection_gateway=tabby_connection_gateway.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='tabby_connection_gateway',
    packages=['tabby_connection_gateway'],
    url='https://github.com/eugeny/tabby_connection_gateway',
    zip_safe=False,
)
