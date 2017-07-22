import os
from setuptools import setup
import sys
from platform import platform

if sys.version_info < (3, 5):
	sys.exit('Sorry, Python < 3.5 is not supported')
if 'Ubuntu' in platform():
	os.system("sudo apt-get install python3-tk")
elif 'Fedora' in platform():
	os.system("sudo yum install python3-tk")
else:
	sys.stderr.write(
	"""
	Error...
	Different OS...
	Download and install python3-tk for your specific OS
	""")
	sys.exit(0)

setup(
    name = "OpenAnalysis",
    version = "0.0.1",
    author = "OpenWeavers",
    description = ("An open source package to analyse and visualise algorithms and data structures"),
    license = "GNU",
    keywords = "OpenWeavers product",
    url = "http://openalgorithm.readthedocs.io",
    packages=['OpenAnalysis'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU License",
    ],
    install_requires=[
	'networkx',
	'numpy',
	'matplotlib',
    ],
    extras_require={
	"extensions" : [
            'jupyter', 
            'ipython',
        ],
    },	
)
