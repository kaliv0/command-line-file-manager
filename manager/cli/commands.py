from typing import Optional

import click

from manager.logs.config import logger_types
from manager.logs.logger_factory import LoggerFactory
from manager.utils import organizer, scanner


# ### scan ###
@click.command()
@click.argument("dir_path", type=click.STRING)
@click.option(
    "--sort",
    type=click.Choice(["name", "size", "date", "modified", "type"], case_sensitive=False),
    default="name",
    show_default=True,
    help="Sorting criteria",
)
@click.option(
    "--desc",
    is_flag=True,
    help="Display result in descending order",
)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def scan_files(dir_path: str, sort: str, desc: bool, save: bool, output: str) -> None:
    """DIR_PATH: Path to directory to be scanned"""

    scanner.scan_files(dir_path, sort, desc, save, output)


@click.command()
@click.argument("dir_path", type=click.STRING)
@click.option(
    "--sort",
    type=click.Choice(["name", "size", "date", "modified"], case_sensitive=False),
    default="name",
    show_default=True,
    help="Sorting criteria",
)
@click.option(
    "--desc",
    is_flag=True,
    help="Display result in descending order",
)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def scan_subdirs(dir_path: str, sort: str, desc: bool, save: bool, output: str) -> None:
    """DIR_PATH: Path to directory to be scanned"""

    scanner.scan_subdirs(dir_path, sort, desc, save, output)


#############################################################
@click.command()
@click.argument("dir_path", type=click.STRING)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def build_catalog(dir_path: str, save: bool, output: str):
    """DIR_PATH: Path to directory to be scanned"""

    message = scanner.build_catalog(dir_path)
    click.echo(message)
    if save:
        _save_logs_to_file(output, dir_path, message, logger_types.CATALOG)


@click.command()
@click.argument("dir_path", type=click.STRING)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def build_catalog_recursively(dir_path: str, save: bool, output: str) -> None:
    """DIR_PATH: Path to directory to be scanned"""

    message = scanner.get_recursive_catalog(dir_path)
    click.echo(message)
    if save:
        _save_logs_to_file(output, dir_path, message, logger_types.RECURSIVE)


#############################################################
@click.command()
@click.argument("dir_path", type=click.STRING)
@click.option(
    "-h",
    "--hidden",
    "show_hidden",
    is_flag=True,
    help="Include hidden files and folders",
)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def build_tree(dir_path: str, show_hidden: bool, save: bool, output: str) -> None:
    """DIR_PATH: Path to directory to be scanned"""

    scanner.build_tree(dir_path, show_hidden, save, output)


@click.command()
@click.argument("dir_path", type=click.STRING)
@click.option(
    "-h",
    "--hidden",
    "show_hidden",
    is_flag=True,
    help="Include hidden files and folders",
)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def build_pretty_tree(dir_path: str, show_hidden: bool, save: bool, output: str) -> None:
    """DIR_PATH: Path to directory to be scanned"""

    scanner.build_pretty_tree(dir_path, show_hidden, save, output)


#############################################################
@click.command()
@click.argument("dir_path", type=click.STRING)
@click.argument("name", type=click.STRING)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def search_by_name(dir_path: str, name: str, save: bool, output: str) -> None:
    """
    Search by NAME inside DIR_PATH
    """

    scanner.search_by_name(dir_path, name, save, output)


@click.command()
@click.argument("dir_path", type=click.STRING)
@click.argument("name", type=click.STRING)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def search_by_name_recursively(dir_path: str, name: str, save: bool, output: str) -> None:
    """
    Search recursively by NAME inside DIR_PATH
    """

    scanner.search_by_name_recursively(dir_path, name, save, output)


@click.command()
@click.argument("dir_path", type=click.STRING)
@click.argument("other_path", type=click.STRING)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def compare_directories(dir_path: str, other_path: str, save: bool, output: str) -> None:
    ...


#############################################################


#############################################################
# ### organize ###
@click.command()
@click.argument("dir_path", type=click.STRING)
@click.option(
    "-x",
    "--exclude",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Single or multiple file extensions to be skipped separated by comma"
    "E.g. --exclude .pdf,.mp3",
)
@click.option(
    "-h",
    "--hidden",
    "show_hidden",
    is_flag=True,
    help="Include hidden files",
)
@click.option(
    "-b",
    "--backup",
    is_flag=True,
    help="Create an archived file of the given directory before re-organizing it",
)
@click.option(
    "-f",
    "--archive-format",
    type=click.Choice(["tar", "zip"], case_sensitive=False),
    default=None,
    show_default=True,
    help="Archive format for backup file",
)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def organize_files(
    dir_path: str,
    exclude: str,
    show_hidden: bool,
    backup: bool,
    archive_format: str,
    save: bool,
    output: str,
) -> None:
    """
    Organize files by extension/type inside DIR_PATH
    """

    organizer.organize_files(dir_path, exclude, show_hidden, backup, archive_format, save, output)


#############################################################
@click.command()
@click.argument("dir_path", type=click.STRING)
@click.option(
    "-x",
    "--exclude",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Single or multiple file extensions to be skipped separated by comma. "
    "E.g. --exclude .pdf,.mp3",
)
@click.option(
    "--exclude-dir",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Single or multiple directory names to be skipped separated by comma. "
    "E.g. --exclude-dir audio,video",
)
@click.option(
    "--flat",
    is_flag=True,
    help="Move all files to target directories inside parent folder",
)
@click.option(
    "-h",
    "--hidden",
    "show_hidden",
    is_flag=True,
    help="Include hidden files and folders",
)
@click.option(
    "-b",
    "--backup",
    is_flag=True,
    help="Create an archived file of the given directory before re-organizing it",
)
@click.option(
    "-f",
    "--archive-format",
    type=click.Choice(["tar", "zip"], case_sensitive=False),
    default=None,
    show_default=True,
    help="Archive format for backup file",
)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def organize_files_recursively(
    dir_path: str,
    exclude: str,
    exclude_dir: str,
    flat: bool,
    show_hidden: bool,
    backup: bool,
    archive_format: str,
    save: bool,
    output: str,
) -> None:
    """
    Organize files recursively by extension/type inside DIR_PATH
    """

    organizer.organize_files_recursively(
        dir_path, exclude, exclude_dir, flat, show_hidden, backup, archive_format, save, output
    )


#####################################
@click.command()
@click.argument("dir_path", type=click.STRING)
@click.option(
    "-i",
    "--interactive",
    is_flag=True,
    help="Prompt for destination file name before merging duplicates",
)
@click.option(
    "-h",
    "--hidden",
    "show_hidden",
    is_flag=True,
    help="Include hidden files",
)
@click.option(
    "-b",
    "--backup",
    is_flag=True,
    help="Create an archived file of the given directory before re-organizing it",
)
@click.option(
    "-f",
    "--archive-format",
    type=click.Choice(["tar", "zip"], case_sensitive=False),
    default=None,
    show_default=True,
    help="Archive format for backup file",
)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def handle_duplicate_files(
    dir_path: str,
    interactive: bool,
    show_hidden: bool,
    backup: bool,
    archive_format: str,
    save: bool,
    output: str,
) -> None:
    """
    Find and clean-up duplicate files inside a PATH
    """

    organizer.handle_duplicate_files(
        dir_path, interactive, show_hidden, backup, archive_format, save, output
    )


#############################################################
@click.command()
@click.argument("dir_path", type=click.STRING)
@click.option(
    "-i",
    "--interactive",
    is_flag=True,
    help="Prompt for destination file name before merging duplicates",
)
@click.option(
    "-h",
    "--hidden",
    "show_hidden",
    is_flag=True,
    help="Include hidden files",
)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
@click.option(
    "-b",
    "--backup",
    is_flag=True,
    help="Create an archived file of the given directory before re-organizing it",
)
@click.option(
    "-f",
    "--archive-format",
    type=click.Choice(["tar", "zip"], case_sensitive=False),
    default=None,
    show_default=True,
    help="Archive format for backup file",
)
def handle_duplicate_files_recursively(
    dir_path: str,
    interactive: bool,
    show_hidden: bool,
    save: bool,
    output: str,
    backup: bool,
    archive_format: str,
) -> None:
    """
    Find and clean-up duplicate files recursively inside a PATH
    """

    organizer.handle_duplicate_files_recursively(
        dir_path,
        interactive,
        show_hidden,
        save,
        output,
        backup,
        archive_format,
    )


#############################################################
def _save_logs_to_file(
    output_dir: Optional[str], dir_path: str, message: str, logger_type: str
) -> None:
    if not output_dir:
        output_dir = dir_path
    LoggerFactory.get_logger(logger_type, output_dir, True).info(message)
