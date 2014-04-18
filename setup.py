# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name="django-wabbajack",
    version=__import__('wabbajack').__version__,
    description=read('DESCRIPTION'),
    license="GPL",
    keywords="django unittest",

    author="Rinat F Sabitov",
    author_email="rinat.sabitov@gmail.com",

    maintainer='Rinat F Sabitov',
    maintainer_email='rinat.sabitov@gmail.com',

    url="https://bitbucket.org/histrio/django-wabbajack",
    package_dir={'wabbajack': 'wabbajack'},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    packages=find_packages(exclude=['example', 'example.*']),
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
    long_description=read('README'),
)
