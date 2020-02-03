# How to setup the virtual environment

## Anaconda

For conda you can just import the needed packages with `.yml` file in this directory with

```bash
$ conda env create -f environment.yml
```

or install the required packages with: `conda install numpy pandas luigi scikit-learn`

## Virtualenv

For a pip environment you can use the `requirements.txt` in this directory to install the dependencies:

```bash
pip install -r requirements.txt
```

or install the required packages with: `pip install numpy pandas luigi scikit-learn`
