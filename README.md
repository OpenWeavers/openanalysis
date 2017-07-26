# Documentation Guidelines

Here are some instructions if you want to contribute to the documentation of `openanalysis`

- All documentation is done in Jupyter Notebook Files (`.ipynb`). We did it because of interactive nature of notebook
- When displaying figures, you should display them in both `svg`and `pdf` formats. Also you should display `matplotlib` figures inline.

      %matplotlib inline
      %config InlineBackend.figure_formats={"svg", "pdf"}
      
- We host the documentation at [read the docs](http://openalgorithm.readthedocs.io/en/latest/)
- It also generates `pdf` files serving as offline documentation
- Documentation generation backend if `sphinx`
- `doc/requirements.txt` contains the the list of tools to be present in build server. __DON'T MODIFY IT WITHOUT KNOWING WHAT YOU ARE DOING__
- `doc/config.py` contains the the build configuration for HTML and PDF output. __DON'T MODIFY IT WITHOUT KNOWING WHAT YOU ARE DOING__
- PdfLaTeX present at build server currently has no support for `svg` files, and `png` image quality is lost in PDF.
- Tetst your documentation locally by installing `sphinx` on your system
