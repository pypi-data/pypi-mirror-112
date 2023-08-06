<div align="center">    
 
# Deep Learning Project Template

<!-- [![Paper](http://img.shields.io/badge/paper-arxiv.1803.08606-B31B1B.svg)](https://arxiv.org/) -->

[![Github all releases](https://img.shields.io/github/downloads/Naereen/StrapDown.js/total.svg)](https://github.com/benjamindkilleen/dlproject/releases/)
[![GitHub release](https://img.shields.io/github/release/benjamindkilleen/dlproject.js.svg)](https://github.com/benjamindkilleen/dlproject/releases/)
[![PyPI](https://img.shields.io/pypi/v/dlproject)](https://pypi.org/project/dlproject/)
[![PyPI version shields.io](https://img.shields.io/pypi/v/dlproject.svg)](https://pypi.python.org/pypi/dlproject/)
[![PyPI license](https://img.shields.io/pypi/l/dlproject.svg)](https://pypi.python.org/pypi/dlproject/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/dlproject.svg)](https://pypi.python.org/pypi/dlproject/)
[![Documentation Status](https://readthedocs.org/projects/dlproject/badge/?version=latest)](http://dlproject.readthedocs.io/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/benjamindkilleen/blob/main/run.ipynb)

_The opinionated deep learning template._

</div>

<div align="left">
 
## Description

`dlproject` believes three things.

1. All code should be documented.
2. All experiments should be logged.
3. Configs are better than constants.

## Installation

These instructions assume you are using a linux machine with at least one GPU (CUDA 11.1).

1. Create a new repository using this template and change to the root directory. For example,

   ```bash
   git clone git@github.com:benjamindkilleen/dlproject.git
   cd dlproject
   ```

2. Install dependencies using either Pip or [Anaconda](https://www.anaconda.com/) (preferred):

   - **Pip:** Install [Pytorch](https://pytorch.org/get-started/locally/) to ensure GPU available. Then:

     ```bash
     pip install -r requirements.txt
     pip install -e .
     ```

   - **Anaconda:** modify `environment.yml` to suit your needs. Then run:

     ```bash
     conda env create -f environment.yml
     conda activate dlproject
     ```

   This will create a new environment with the project installed as an edit-able package.

### Configure

TODO: locations that need attention.

## Usage

The project is separated into "experiments," which are just different `main` functions using the `vertview` library. Everything should be run through hydra, specifying the `experiment` group parameter. For example:

```bash
python main.py experiment=mnist
```

### Documentation

Documentation and tutorials for `dlproject` are available [here](https://dlproject.readthedocs.io/). You should document your code as you go. If you use Visual Studio Code, [this](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) is an extension which will create Google style docstrings automatically.

To build the docstrings you write into a local static web-page, run

```bash
pip install -r docs/requirements.txt
sphinx-apidoc -f -o docs/source dlproject
cd docs
make html
```

And open `/docs/build/html/index.html` in your browser.

### Citation

```
@article{YourName,
  title={Your Title},
  author={Your team},
  journal={Location},
  year={Year}
}
```

</div>
