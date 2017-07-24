# Setup for openanalysis
import os
from setuptools import setup
import sys
from platform import platform
#Python3 installations
if sys.version_info < (3, 5):
    if 'Ubuntu' in platform() or 'Debian' in platform():
        os.system("sudo apt-get install python3 python3-pip")
    else:
         os.system("sudo yum install python3 python3-pip")
pkgs = ["python3-tk", "ffmpeg", "python-gi-cairo"]
if 'Ubuntu' in platform() or 'Debian' in platform():
    import apt
    cache = apt.cache.Cache()
    cache.update()
    for pkg in pkgs:
        cpkg = cache[pkg]
        if cpkg.is_installed:
            print("{0} already installed".format(pkg))
        else:
            cpkg.mark_install()
        try:
            cache.commit()
        except Exception as e:
            sys.stderr.write("Couldn't install {0} due to {1}".format(pkgs, e))
elif 'Fedora' in platform():
    import yum
    yb = yum.YumBase()
    inst = yb.rpmdb.returnPackages()
    installed = [x.name for x in inst]
    for pkg in pkgs:
        if pkg in installed:
            print("{0} is already installed".format(pkg))
        else:
            print("Installing {0}".format(pkg))
            kwarg = {
                'name': pkg
            }
            yb.install(**kwarg)
            yb.resolveDeps()
            yb.buildTransaction()
            yb.ProcessTransaction()
else:
    sys.stderr.write(
        """
        Error...
        Unsupported OS...
        Download and install python3-tk, ffmpeg and python-gi-cairo for your OS
        """)
    sys.exit(0)

setup(
    name="openanalysis",
    version="0.0.3",
    author="OpenWeavers",
    description="An open source package to analyse and visualise algorithms and data structures",
    license="GPLv3+",
    keywords="OpenWeavers product",
    url="https://github.com/OpenWeavers/OpenAlgorithm",
    packages=['openanalysis',
              'analysistest',
    ],
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
    ],
    extras_require={
        "extensions": [
            'jupyter',
            'ipython',
        ],
    },
)
