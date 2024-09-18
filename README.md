# command-line-file-manager

[![PyPI](https://img.shields.io/pypi/v/command-line-file-manager.svg)](https://pypi.org/project/command-line-file-manager/)
[![Downloads](https://static.pepy.tech/badge/command-line-file-manager)](https://pepy.tech/project/command-line-file-manager)

Python CLI tool for scanning and organizing local directories and files.

#### Requires Python 3.10+

## Installation


Via pip:
```console
$ pip install command-line-file-manager
```

From main branch:
```console
$ git clone https://github.com/kaliv0/command-line-file-manager.git
$ cd command-line-file-manager 
$ pip install .
```

## Example


To run the application type <i>fm</i> followed by a sub-command, target directory and options
```console
$ fm scan-files ../test --sort=type --save --output=./
```

Add --help after the <i>fm</i> command or any of the subcommands to get more information
```console
$ fm scan-files --help

Usage: fm scan-files [OPTIONS] DIR_PATH

  DIR_PATH: Path to directory to be scanned

Options:
  --sort [name|size|date|modified|type]   Sorting criteria.  [default: name]
  --desc                                  Display result in descending order.
  -s, --save                              Save log message to file.
  -o, --output TEXT                       Path to output directory for the saved log file.
  --help                                  Show this message and exit.
```
