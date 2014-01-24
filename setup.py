import re

from os.path import join, dirname
from distutils.core import setup
from pip.req import parse_requirements

README = open(join(dirname(__file__), 'README.rst')).read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(join(package, '__init__.py')).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)


def get_requirements():
    reqs = parse_requirements(join(dirname(__file__), 'requirements.txt'))
    requirements = [str(ir.req) for ir in reqs]
    return requirements


setup(
    name='django-vmail',
    version=get_version('vmail'),
    description="Virtual mail administration django app",
    author="Lewis Gunsch",
    author_email="lewis@gunsch.ca",
    url="https://github.com/lgunsch/django-vmail/",
    license='MIT',
    long_description=README,
    packages=[
        'vmail',
        'vmail.management',
        'vmail.management.commands',
        'vmail.migrations',
        'vmail.tests',
    ],
    scripts=[],
    install_requires=get_requirements(),
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications :: Email',
        'Topic :: Communications :: Email :: Mail Transport Agents',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
