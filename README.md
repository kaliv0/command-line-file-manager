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

## Example

To run the application type <i>fm</i> followed by a sub-command, target directory and options
```console
$ fm scan ./foo/bar --sort=type --save --output=./
```

```console
$ fm scan --help

Usage: fm scan <options> <dir_path>

  Create full catalog of all files and subdirs in <dir_path>

Options:
  -r, --recursively               Build catalog recursively
  --sort [name|size|date|modified|type]
                                  Sorting criteria
  --desc                          Display result in descending order
  -s, --save                      Save log message to file
  -o, --output TEXT               Path to output directory for the saved log file
  --log TEXT                      Saved log file name
  --help                          Show this message and exit
```

## Main Features
- <b>show</b> -   Short list of files or directories in <dir_path>
- <b>scan</b> -   Create full catalog of all files and subdirs in <dir_path>
- <b>tree</b> -   Build tree of contents in <dir_path>
- <b>search</b> - Search by <given_name> inside <dir_path>
- <b>diff</b> -   Compare contents of <source_path> to <target_path>
- <b>dedup</b> -  Find and clean-up duplicate files inside a <dir_path>
- <b>tidy</b> -   Organize files by extension/type inside <dir_path>
