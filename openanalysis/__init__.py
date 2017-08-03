import os


__all__ = ["base_data_structures", "datastructures.py", "matrix_animator", "searching", "sorting", "string_matching", "tree_growth"]
pkgs = []

if not os.path.exists("check_file"):
    print(
        """
    The OpenAlgorithm library needs 'libgraphviz-dev', 'pkg-config', 'python3-tk', 
    and 'ffmpeg' packages to be installed for graph visualization.
   
    Install them before continuing...
    """)

    with open("check_file", 'w') as f:
        f.write("")
