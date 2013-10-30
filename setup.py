import os

from distutils.core import setup

VERSION = '0.1.0'

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

required = [
    'Django >= 1.5.0',
]

setup(
    name='madmin',
    version=VERSION,
    description="Virtual mail administration django app",
    author="Lewis Gunsch",
    author_email="lewis@gunsch.ca",
    url="https://github.com/lgunsch/madmin",
    license='LICENSE.md',
    long_description=README,
    packages=[
        'madmin',
        'madmin.management',
        'madmin.management.commands',
        'madmin.migrations',
    ],
    scripts=[],
    install_requires=required,
)
