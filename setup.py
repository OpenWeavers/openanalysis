# Setup for openanalysis
import os
from setuptools import setup
import sys
import subprocess
#Python3 installations

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_path(path=None):
    if path != None:
        return(os.path.join('openanalysis', 'string_matching_samples', path))
    else:
        return(os.path.join('openanalysis', 'string_matching_samples'))

pkg_dict = {
    "ffmpeg": "ffmpeg", 
    "graphviz": "dot"}
pkg_avail = {pkg:True for pkg in pkg_dict}

for pkg in pkg_dict:
    try:
        subprocess.Popen(pkg_dict[pkg], stdout=subprocess.DEVNULL)
    except FileNotFoundError:
        pkg_avail[pkg] = False  

setup(
    name="OpenAnalysis",
    version="0.0.5",
    author="OpenWeavers1",
    author_email="srmonish96@gmail.com",
    description="An open source package to analyse and visualise algorithms and data structures",
    license="GPLv3+",
    keywords="OpenWeavers product",
    url="https://github.com/OpenWeavers/OpenAlgorithm",
    packages=['openanalysis',
    ],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.5",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
    install_requires=[
        'networkx',
        'numpy',
        'matplotlib',
        'pygraphviz',
    ],
    extras_require={
        "extensions": [
            'jupyter',
            'ipython',
        ],
    },
    data_files=[(get_path(), [get_path(x) for x in os.listdir(get_path())])]
)

for pkg in pkg_dict:
    if not pkg_avail[pkg]:
        sys.stderr.write("""
WARNING
-------

Package %(pkg) not found...
Please install
""" %{"pkg", pkg})
		
