pkgs = ["libgraphviz-dev", "pkg-config", "python3-tk", "ffmpeg"]

print(
    """
    The OpenAlgorithm library needs {0}, {1}, {2}, and {3}
    packages to be installed for graph visualization.
   
    Install them before continuing...
    """
.format(pkgs))
