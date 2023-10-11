# command-line-file-manager

Python CLI tool for scanning and organizing local folders and files.

#### Requires Python 3.11+

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

```console
Usage: fm scan-files [OPTIONS] DIR_PATH

  DIR_PATH: Path to directory to be scanned

Options:
  --sort [name|size|date|modified|type]   Sorting criteria.  [default: name]
  --desc BOOLEAN                          Boolean flag to display result in descending order.
                                          [default: False]
  -s, --save BOOLEAN                      Boolean flag to save log message to file.
                                          [default: False]
  -o, --output TEXT                       Path to output directory for the saved log file.
  --help                                  Show this message and exit.
```
