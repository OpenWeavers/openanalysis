# Documentation Guidelines

Here are some instructions if you want to contribute to the documentation of `openanalysis`:

- All documentation is done in Jupyter Notebook Files (`.ipynb`). It is done because of the interactive nature of notebook.
- When displaying figures, you should display them in both `svg`and `pdf` formats. Also you should display `matplotlib` figures inline.

      %matplotlib inline
      %config InlineBackend.figure_formats={"svg", "pdf"}
      
- Documentation is hosted at [read the docs](http://openalgorithm.readthedocs.io/en/latest/).
- It also generates `pdf` files serving as offline documentation.
- Documentation generation backend is `sphinx`.
- `doc/requirements.txt` contains the the list of tools to be present in build server. __DON'T MODIFY IT WITHOUT KNOWING WHAT YOU ARE DOING__
- `doc/config.py` contains the the build configuration for HTML and PDF output. __DON'T MODIFY IT WITHOUT KNOWING WHAT YOU ARE DOING__
- PDFLaTeX present at build server currently has no support for `svg` files, and `png` image quality is lost in PDF.
- Test your documentation locally by installing `sphinx` on your system.
- `pull` the latest version of repo before starting documentation. By not doing this, __CHANCES ARE HIGH THAT OTHERS' MODIFICATIONS ARE LOST__
