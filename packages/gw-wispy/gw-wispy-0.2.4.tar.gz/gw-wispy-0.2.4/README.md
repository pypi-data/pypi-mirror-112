# wispy

Neural Network Based Waveform Modelling

pypi - https://pypi.org/project/gw-wispy/

## Installation

```
pip install gw-wispy
```

## Development

```
conda create -n wispy python=3.7
conda activate wispy
pip install tensorflow lalsuite pycbc matplotlib tensorflow-addons tqdm gw-phenom
```

## Upload to pypi

```
python setup.py clean --all
rm -rf dist/
python3 setup.py sdist bdist_wheel
python3 -m twine upload  dist/*
```
