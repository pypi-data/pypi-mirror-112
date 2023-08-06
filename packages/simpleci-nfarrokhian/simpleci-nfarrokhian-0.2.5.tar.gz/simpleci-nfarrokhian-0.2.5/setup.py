#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = [ ]

setup(
    author="Nathan Farrokhian",
    author_email='n.farrokhian@gmail.com',
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
    ],
    description="generates concentration curves from ordered data and calculates concentration indices (ACI and RCI)",
    entry_points={
        'console_scripts': [
            'simpleci=simpleci.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='simpleci',
    name='simpleci-nfarrokhian',
    packages=find_packages(include=['simpleci', 'simpleci.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/nfarrokhian/simpleci',
    version='0.2.5',
    zip_safe=False,
)
