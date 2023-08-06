
import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "paper-network",
    version = "0.0.1",
    description = "Gibbs Sampler and other functions for PAPER (Preferential Attachment Plus Erdos--Renyi) model for random networks",
    packages = setuptools.find_packages(include=['PAPER']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering'
    ],
    author = "Min Xu",
    author_email = "mx76@stat.rutgers.edu",
    url = 'https://github.com/nineisprime/PAPER',
    install_requires = [
        'python-igraph',
        'numpy'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown"
)
