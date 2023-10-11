# command-line-file-manager

Python CLI tool for scanning and organizing local folders and files.

## Requirements

Python 3.11+

## Installation


Via pip:
```console
$ python -m pip install command-line-file-manager
```

From master branch:
```console
$ git clone https://github.com/Mithras11/command-line-file-manager.git
$ cd command-line-file-manager 
$ python -m pip install .
```

## Example


To run the application type <i>fm</i> followed by a sub-command, target directory and options
```console
$ fm scan-files ../test --save=true --output=./ --sort=type
```

Add --help after the <i>fm</i> command or any of the subcommands to get more information
```console
$ fm scan-files --help
```

Usage: main.py [OPTIONS] NAME

```console
╭─ Arguments ───────────────────────────────────────╮
│ *    name      TEXT  [default: None] [required]   |
╰───────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────╮
│ --help          Show this message and exit.       │
╰───────────────────────────────────────────────────╯
```
