#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Subhendu Ranjan Mishra",
    author_email='subhendu.r.mishra@hotmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="Torrent CLI Client application",
    entry_points={
        'console_scripts': [
            'torrent_client_cli=torrent_client_cli.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='torrent_client_cli',
    name='torrent_client_cli',
    packages=find_packages(include=['torrent_client_cli', 'torrent_client_cli.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/subhrm/torrent_client_cli',
    version='0.1.0',
    zip_safe=False,
)
