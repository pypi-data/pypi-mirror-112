from setuptools import setup, find_packages


setup(
    name='tbridge',
    version='1.5.1',
    license='BSD',
    author="Harrison Souchereau",
    author_email='harrison.souchereau@yale.edu',
    packages=find_packages('tbridge'),
    package_dir={'': 'tbridge'},
    url='https://github.com/HSouch/TBRIDGE',
    keywords='galaxies surface brightness profiles',
    install_requires=[
          'scikit-image', 'numpy', 'photutils', 'astropy', 'pebble', 'tqdm'
      ],

)