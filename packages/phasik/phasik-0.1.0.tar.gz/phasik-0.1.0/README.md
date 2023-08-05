[![Documentation Status](https://readthedocs.org/projects/phasik/badge/)](http://phasik.readthedocs.io/)
[![PyPI version](https://badge.fury.io/py/phasik.svg)](https://badge.fury.io/py/phasik)
[![PyPI license](https://img.shields.io/pypi/l/phasik.svg)](https://pypi.python.org/pypi/phasik/)

# Code for the paper | "Inferring cell cycle phases from a temporal network of protein interactions"

The code contains
- Phasik, our general-use package to infer phases in temporal networks
- the notebooks use in our analysis for the paper, which uses Phasik

Authors of the paper: Maxime Lucas, Alex Townsend-Teague, Arthur Morris, Laurent Tichit, Bianca Habermann,  Alain Barrat

Contributors to Phasik: Maxime Lucas, Alex Townsend-Teague, Arthur Morris

#### What is Phasik?
The Phasik package was created to infer temporal phases in temporal networks.  It contains various utility classes and functions that can be divided into two main parts:

1. Build, analyse, and visualise temporal networks from time series data.
2. Infer temporal phases by clustering the snapshots of the temporal network.

### Install Phasik 

Install the latest version of `phasik` with `pip`:

```
$ pip install phasik
```

Alternatively, you can clone the repository manually or with `git`, and then install with `pip`:
```    
$ git clone https://gitlab.com/habermann_lab/phasik.git  
$ pip install ./phasik
```   
You can also simply try `phasik` by cloning the repository without installing the package.

### Documentation

The full documentation of the package is available at <https://phasik.readthedocs.io/en/latest/>, together with tutorials.

