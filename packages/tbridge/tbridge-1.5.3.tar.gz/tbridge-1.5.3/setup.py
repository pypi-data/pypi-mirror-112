
from distutils.core import setup
from setuptools import find_packages

setup(
    name = 'tbridge',
    packages = find_packages(),
    version = '1.5.3',
    license='BSD-3-Clause',
    description = 'Simulation suite for efficiency testing of galaxy surface brightness profiles.',
    author="Harrison Souchereau",
    author_email='harrison.souchereau@yale.edu',
    url='https://github.com/HSouch/TBRIDGE',
    keywords='galaxies surface brightness profiles',
    install_requires=[
        'scikit-image',
        'numpy',
        'photutils',
        'astropy',
        'pebble',
        'tqdm'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

    ],
)