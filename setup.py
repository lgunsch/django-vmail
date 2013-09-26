import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

required = [
    'Django==1.5.4',
]

setup(
    name='madmin',
    version='0.1.0',
    packages=[
        'madmin'
    ],
    description="Virtual mail administration django app",
    long_description=README,
    author="Lewis Gunsch",
    scripts=[],
    install_requires=required,
)
