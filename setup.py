# Setup for openanalysis
import os
from setuptools import setup
import sys
import subprocess

if sys.version_info[:2] < (3, 5):
    sys.stderr.write("""
ERROR
-----
This package can be run only by python>=(3, 5)
Replace python=={} by python>=(3, 5)
""".format(sys.version_info[:2]))
    sys.exit(1)
    
def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


pkg_dict = {
    "ffmpeg": "ffmpeg",
    "graphviz": "dot"
}

pkg_avail = {pkg: True for pkg in pkg_dict}

for pkg in pkg_dict:
    try:
        test_process = subprocess.Popen(pkg_dict[pkg], stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL)
        subprocess.Popen.kill(test_process)
    except FileNotFoundError:
        pkg_avail[pkg] = False

setup(
    name="OpenAnalysis",
    version="0.0.8",
    author="OpenWeavers1",
    author_email="srmonish96@gmail.com",
    description="An open source package to analyse and visualise algorithms and data structures",
    license="GPLv3+",
    keywords="OpenWeavers product",
    url="https://github.com/OpenWeavers/OpenAlgorithm",
    packages=['openanalysis', ],
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
        'progressbar2',
    ],
    extras_require={
        "extensions": [
            'jupyter',
            'ipython',
        ],
    },
    include_package_data=True,
)

for pkg in pkg_dict:
    if not pkg_avail[pkg]:
        sys.stderr.write("""
WARNING
-------

Package {0} not found...
Please install
""".format(pkg))
