#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'h2',
    'curio'
]

test_requirements = [
    'pytest'
]

setup(
    name='hyper2web',
    version='0.0.6',
    description="Coroutine based H2 Web backend framework built for the future.",
    long_description=readme + '\n\n' + history,
    author="Xuanzhe Wang",
    author_email='wangxuanzhealbert@gmail.com',
    url='https://github.com/CreatCodeBuild/hyper2web',
    packages=[
        'hyper2web',
    ],
    package_dir={'hyper2web': 'hyper2web'},
    entry_points={
        'console_scripts': [
            'hyper2web=hyper2web.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='hyper2web',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
