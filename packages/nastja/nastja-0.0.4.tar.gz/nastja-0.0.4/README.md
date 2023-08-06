# Python interface for the NAStJA

[NAStJA](https://gitlab.com/nastja/nastja/) is an HPC simulation framework for various domains. This python packages is intended to provides an easy access to use python scripts for the pre- and post-processing steps of NAStJA simulations.

## The io module
NAStJA produce different output files all collected in one output directory. Create a `SimDir(output directory)` to access the output files:
* Parallel output vti can be read via `readVTI(frame)` as a pyVista object.
* Cell info cvs data can be read via `readCSV(frame)` as a pandas dataframe.
* Squeezed cell info data in a SQLite database can be read via `readSQL(frame)` as a pandas dataframe.
* `query(string)` is used to make arbitrary queries.

All other data are currently unsupported. Use the parallel vti output instead the block-wise vti output.

#### Development notes
You can install this local package editable for the development via `pip3 install -e .`

Use `python3 -m build` to build the package and `python3 -m twine upload dist/*` to upload it to PyPI.
