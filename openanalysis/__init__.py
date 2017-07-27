import sys
from platform import platform

pkgs = ["libgraphviz-dev", "pkg-config", "python3-tk", "ffmpeg"]
to_be_installd = []
platform_check = 0

if 'Ubuntu' in platform() or 'Debian' in platform():
    import apt
    platform_check += 1
    cache = apt.cache.Cache()
    cache.update()  #needs sudo permissions
    for pkg in pkgs:
        cpkg = cache[pkg]
        if not cpkg.is_installed:
            to_be_installd.append(pkg)

elif 'Fedora' in platform():
    import yum
    platform_check += 1
    yb = yum.YumBase()
    inst = yb.rpmdb.returnPackages()
    installed = [x.name for x in inst]
    for pkg in pkgs:
        if pkg not in installed:
            to_be_installd.append(pkg)

else:
    to_be_installd.append('-1')

if len(to_be_installd) == 0 and platform_check != 0:
    print("The following package(s) are not installed:\n", ', '.join(to_be_installd))
    print(
    """
    The OpenAlgorithm library needs these packages
    to be installed for graph visualization.
   
    Do you want to install them now? : (Y / N)
    """)
    
    choice = input().capitalize()
    
    try:
        if choice == 'Y':
            if 'Ubuntu' in platform() or 'Debian' in platform():
                for pkg in to_be_installd:
                    print("Installing {0}".format(pkg))
                    pkg.mark_install()
                    cache.commit()
            
            elif 'Fedora' in platform():
                print("Installing {0}".format(pkg))
                kwarg = {
                    'name': pkg
                }
                yb.install(**kwarg)
                yb.resolveDeps()
                yb.buildTransaction()
                yb.ProcessTransaction()

            else:
                print(
                """
                Unsupported OS...
                Make sure to download and install python3-tk, libgraphviz-dev, pkg-config, and ffmpeg for your OS
                if you haven't already before continuing.
                (Press Ctrl+D to exit out of the shell)
                """)

        else:
            sys.exit(1)
            
    except Exception as e:
        sys.stderr.write("Couldn't install {0} due to {1}".format(pkg, e))
        sys.exit(1)
