# Executable I/O Testing Tool (exiot)

The (`exiot`) is a testing tool to test the executable `STDIN`, `STDOUT`, `STDERR`, and many more.

## Getting Started

In order to install the latest "stable" version of the tool you can use the [pip](https://packaging.python.org/tutorials/installing-packages/).

```shell
pip install exiot
```

In order to get latest version of the tool you can just clone the repository:

```shell
git clone https://github.com/pestanko/exiot.git
```

and then use the [poetry](https://python-poetry.org/docs/) to install dependencies, or just install them manually (dependencies are optional).

```shell
cd exiot
poetry install
```

Optional dependencies:

- ``junitparser`` - to produce the junit report
- ``pyyaml`` - to parse yaml schemas and generate yaml reports

You can install them manually if you do not want to use the poetry

```shell
pip install junitparser pyyaml 
```

## Usage

Show help:
```shell
$ python -m exiot --help
```

### Parse the tests

Parse the tests - show all available tests:

```shell
python -m exiot parse tests/prepared_data/single_fail
```

Parse the tests - show all available tests, dump them as `json` or `yaml` (if `pyyaml` installed):

```shell
python -m exiot parse -o json tests/prepared_data/single_fail
# or yaml if PyYAML installed
python -m exiot parse -o yaml tests/prepared_data/single_fail
```

### Run the tests

Run tests in directory:

```shell
python -m exiot -Linfo exec -E ./myexec ./tests
```

Run Mini Homeworks:

```shell
# -p parameters specifies the "parser" - minihw is special parser for parsing the mini homeworks for FI:PB071
python -m exiot -Linfo exec -p minihw /home/user/src/c/mini05
```
