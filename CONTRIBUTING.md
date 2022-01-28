# Contributing

## How to setup development environment

1. Fork and clone into the git repository.
2. Make a virtual environment.
```sh
python -m venv .venv
```
3. Activate the virtual environment (How to do this deepends on the OS and shell).
4. Install the development packages.
```sh
pip install --upgrade pip
pip install -r dev_requirements.txt
```
5. Setup `pre-commit`.
```sh
pre-commit install
```
6. Install the package in editable mode.
```sh
pip intall -e .
```
7. Start coding.
