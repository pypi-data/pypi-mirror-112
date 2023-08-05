# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oommfpy', 'oommfpy.tools']

package_data = \
{'': ['*'], 'oommfpy.tools': ['clib/*']}

install_requires = \
['Cython>=0.29.23,<0.30.0',
 'click>=7.1,<8.0',
 'matplotlib>=3.3.4,<4.0.0',
 'numpy>=1.20.3,<2.0.0',
 'scipy>=1.6.3,<2.0.0']

entry_points = \
{'console_scripts': ['omf2vtk = oommfpy.tools.omf2vtk:omf2vtk_cli',
                     'plot_omf = '
                     'oommfpy.tools.plot_slices:plot_omf_slices_cli']}

setup_kwargs = {
    'name': 'oommfpy',
    'version': '1.2',
    'description': 'Minimal Python lib to process OOMMF format output files',
    'long_description': "[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2611194.svg)](https://doi.org/10.5281/zenodo.2611194)\n\n```\n   .+------+-------+-------+-------+-------+-------+-------+\n .'      .'      .'      .'      .'      .'      .'      .'|\n+---+--+'------+'------+'------+'------+'------+'------+'  -\n|      |       |       |       |       |       |       |   |\n|   O  +   O   +   M   +   M   +   F   +   P   +   Y   +   +\n|      |       |       |       |       |       |       | .'\n+------+'------+'------+'------+-------+-------+-------+'\n```\n\n# OOMMFPy\n\nA very minimal and simple Python library to read and extract data from OOMMF\nmagnetisation files `omf`, which are also used in MuMax3. In addition to this\nlibrary we provide tools to plot `omf` files and convert them to `vtk` files.\n\nHighlights:\n\n- Read `omf` files in any format\n- Can also read `ovf` files and MuMax3 files\n- Painless conversion of the data in an `omf` file into Numpy arrays for data\n  analysis\n- Fast calculation (using Numpy) of the skyrmion number in a slice of the\n  system in any plane orientation (`xy`, `xz`, `yz`)\n- Fast reading of `omf` files in binary format (using Numpy's `fromfile`)\n- Minimal and super fast tool to convert `omf` files to VTK format\n- Plot functions\n- Early support for Paraview plugin: read `omf` files directly!\n\n## Install\n\nThe easiest is to use `pip` or `poetry` to install the package from\n[PyPI](https://pypi.org/project/oommfpy)\n\n    pip install oommfpy\n\nThe Github address can also be directly used to install the package via `pip`\n\n    pip install git+https://github.com/davidcortesortuno/oommfpy\n\nAlternatively, a `setup.py` file is provided to install this library\n\n    git clone https://github.com/davidcortesortuno/oommfpy\n    cd oommfpy\n    pip install ./\n\nIf successful, the `plot_omf` and `omf2vtk` tools are installed in the\ncorresponding `bin` directory and can be called from the command line.\n\nA C library is built with the installation process, thus the setup file tries\nto install Cython if is not present in the system.\n\n### Paraview plugin\n\nA first version of a reader for Paraview is added in this last version. For now\nthe installation is a bit of a hack:\n\n- After installing the `oommfpy` library, locate the `oommfpy` folder from\n  the`site-packages` directory\n\n- Download the latest version of Paraview with Python > 3.8 support\n\n- Copy the `oommfpy` directory into the Paraview Python `site-packages` folder.\n  For example, for Paraview 5.9.0 installed in the `home` folder:\n\n  ```\n  cp -r oommfpy $HOME/ParaView-5.9.0-MPI-Linux-Python3.8-64bit/lib/python3.8/site-packages/\n  ```\n\n- Open Paraview and go to `Tools -> Manage Plugins -> Load New` and select the\n  Python file in the `tools/` folder of `oommfpy` (you can clone the\n  repository)\n\n- Now you can open any `omf` file without converting to VTK!\n\n## Documentation\n\nFor now check the `doc/ipynb` folder which contains a tutorial with basic\nfunctionality. To load a file with a magnetisation field, which is found more\ncommonly in simulations, use the `MagnetisationData` class. To load any field,\nsuch as the dipolar field, use the `FieldData` class.\n\nScripts to convert `omf` to VTK can be called directly as, for example,\n\n```\nomf2vtk -i omfs/my_oommf_output.omf -o test.vtk\n```\n\nThe input path can also be a directory or a path with a wildcard, *e.g.*\n`omfs/*.omf`. This method assumes the files in the path come from the same\nsimulation as the tool loads the mesh from the first file in the path and then\nonly updates the magnetisation fields.\n\nSimilar options are provided for the `plot_omf` function. Use the `--help` for\ndetails.\n\n## TODO\n\n- [ ] More tests\n- [ ] Add pyproject.toml file to avoid manual installation of Cython in setup.py\n- [ ] More options to plotting library\n- [ ] Print `z` coordinate when computing sk number\n- [ ] Allow Periodic boundaries for the skyrmion number calculation\n- [ ] Add typing check\n- [ ] Support for multiple OS\n\n# Citation\n\nIf you find this library useful, please cite this repository as:\n\n```\n@Misc{Cortes2019,\n  author       = {David Cort{\\'e}s-Ortu{\\~n}o},\n  title        = {OOMMFPy},\n  howpublished = {Zenodo doi:10.5281/zenodo.2611194. Github: https://github.com/davidcortesortuno/oommfpy},\n  year         = {2019},\n  doi          = {10.5281/zenodo.2611194},\n  url          = {https://doi.org/10.5281/zenodo.2611194},\n}\n```\n",
    'author': 'David Cortés-Ortuño',
    'author_email': 'd.i.cortes@uu.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/davidcortesortuno/oommfpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
