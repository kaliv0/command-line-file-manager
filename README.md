<p align="center">
  <img src="https://github.com/kaliv0/command-line-file-manager/blob/main/assets/fm-snake.jpg?raw=true" alt="Manager">
</p>

---

# command-line-file-manager

[![PyPI](https://img.shields.io/pypi/v/command-line-file-manager.svg)](https://pypi.org/project/command-line-file-manager/)
[![Downloads](https://static.pepy.tech/badge/command-line-file-manager)](https://pepy.tech/projects/command-line-file-manager)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](https://github.com/kaliv0/command-line-file-manager/blob/main/LICENSE)

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

## Main Features
- <b>scan_files</b> - list all files inside PATH
- <b>scan_subdirs</b> - list all nested directories
- <b>build_catalog</b> - list all contents (files, subdirs) 
<br>(can be done recursively via <b>build_catalog_recursively</b>)
- <b>build_tree</b> - visualize directory structure
- <b>build_pretty_tree</b> - a fancy alternative with emojis etc.
-------------------------------
- <b>search_by_name</b>
- <b>search_by_name_recursively</b>
-------------------------------
- <b>organize_files</b> - group files by extension into corresponding 'type' directories (e.g. music, books)
<br>(provides recursive version)

- <b>handle_duplicate_files</b> - merge identical files (in terms of content) - prompts user for file name or uses first entry in duplicates list
<br>(has a recursive alternative)
