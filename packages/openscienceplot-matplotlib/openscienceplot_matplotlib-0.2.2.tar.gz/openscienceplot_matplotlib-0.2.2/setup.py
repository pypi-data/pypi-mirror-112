
from setuptools import setup
from setuptools import find_packages

setup(
    name = 'openscienceplot_matplotlib',
    license = 'MIT',
    author = 'Tom de Geus',
    author_email = 'tom@geus.me',
    description = 'Store data from a matplotlib plot.',
    long_description = 'Store data from a matplotlib plot.',
    keywords = 'matplotlib, hdf5, h5py',
    url = 'https://github.com/tdegeus/openscienceplot_matplotlib',
    packages = find_packages(),
    use_scm_version = {'write_to': 'openscienceplot_matplotlib/_version.py'},
    setup_requires = ['setuptools_scm'],
    install_requires=['matplotlib', 'numpy', 'h5py'])
