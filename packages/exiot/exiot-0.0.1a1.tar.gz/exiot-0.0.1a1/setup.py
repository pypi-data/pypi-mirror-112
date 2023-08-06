# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['exiot']
install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'junitparser']

entry_points = \
{'console_scripts': ['exiot = exiot:main']}

setup_kwargs = {
    'name': 'exiot',
    'version': '0.0.1a1',
    'description': "The 'exiot' is a testing tool to test the executable STDIN, STDOUT, STDERR, and many more.",
    'long_description': '# Executable I/O Testing Tool (exiot)\n\nThe (`exiot`) is a testing tool to test the executable `STDIN`, `STDOUT`, `STDERR`, and many more.\n\n## Getting Started\n\nIn order to install the latest "stable" version of the tool you can use the [pip](https://packaging.python.org/tutorials/installing-packages/).\n\n```shell\npip install exiot\n```\n\nIn order to get latest version of the tool you can just clone the repository:\n\n```shell\ngit clone https://github.com/pestanko/exiot.git\n```\n\nand then use the [poetry](https://python-poetry.org/docs/) to install dependencies, or just install them manually (dependencies are optional).\n\n```shell\ncd exiot\npoetry install\n```\n\nOptional dependencies:\n\n- ``junitparser`` - to produce the junit report\n- ``pyyaml`` - to parse yaml schemas and generate yaml reports\n\nYou can install them manually if you do not want to use the poetry\n\n```shell\npip install junitparser pyyaml \n```\n\n## Usage\n\nShow help:\n```shell\n$ python -m exiot --help\n```\n\n### Parse the tests\n\nParse the tests - show all available tests:\n\n```shell\npython -m exiot parse tests/prepared_data/single_fail\n```\n\nParse the tests - show all available tests, dump them as `json` or `yaml` (if `pyyaml` installed):\n\n```shell\npython -m exiot parse -o json tests/prepared_data/single_fail\n# or yaml if PyYAML installed\npython -m exiot parse -o yaml tests/prepared_data/single_fail\n```\n\n### Run the tests\n\nRun tests in directory:\n\n```shell\npython -m exiot -Linfo exec -E ./myexec ./tests\n```\n\nRun Mini Homeworks:\n\n```shell\n# -p parameters specifies the "parser" - minihw is special parser for parsing the mini homeworks for FI:PB071\npython -m exiot -Linfo exec -p minihw /home/user/src/c/mini05\n```\n',
    'author': 'Peter Stanko',
    'author_email': 'peter.stanko0@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pestanko/exiot',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
