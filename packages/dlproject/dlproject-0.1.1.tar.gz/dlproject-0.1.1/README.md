<div align="center">    
 
# Deep Learning Project Template

<a href="https://github.com/benjamindkilleen/dlproject/releases/">
    <img src="https://img.shields.io/github/downloads/benjamindkilleen/dlproject/total.svg" alt="Downloads" />
</a>
<a href="https://github.com/benjamindkilleen/dlproject/releases/">
    <img src="https://img.shields.io/github/release/benjamindkilleen/dlproject.svg" alt="GitHub release" />
</a>
<a href="https://pypi.org/project/dlproject/">
    <img src="https://img.shields.io/pypi/v/dlproject" alt="PyPI" />
</a>
<a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" />
</a>
<a href="http://dlproject.readthedocs.io/?badge=latest">
    <img src="https://readthedocs.org/projects/dlproject/badge/?version=latest" alt="Documentation Status" />
</a>
<a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black" />
</a>
<a href="https://colab.research.google.com/github/benjamindkilleen/blob/main/run.ipynb">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" />
</a>

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

2. Install dependencies using either [Anaconda](https://www.anaconda.com/) (preferred) or Pip:

   - **Anaconda:** modify `environment.yml` to suit your needs. Then run:

     ```bash
     conda env create -f environment.yml
     conda activate dlproject
     ```

     This will create a new environment with the project installed as an edit-able package.

   - **Pip:** Install [Pytorch](https://pytorch.org/get-started/locally/) to ensure GPU available. Then:

     ```bash
     pip install -r requirements.txt
     pip install -e .
     ```

## Usage

The project is separated into "experiments," which are just different `main` functions. Use the `experiment` group parameter to change which experiment is running. For example:

```bash
python main.py experiment=mnist
```

The results are then neatly sorted into the newly-created `results` directory (ignored by default). This is important for reproduceability, utilizing Hydra's automatic logging and config storage.

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
