#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Cutewarriorlover",
    author_email='cutewarriorlover@gmail.com',
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
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    description="DocSwitch gives you the freedom to write your Python documentation in any format you want, switching between them effortlessly.",
    entry_points={
        'console_scripts': [
            'doc_switch=doc_switch.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='doc_switch',
    name='doc_switch',
    packages=find_packages(include=['doc_switch', 'doc_switch.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/cutewarriorlover/doc_switch',
    version='0.1.1',
    zip_safe=False,
)
