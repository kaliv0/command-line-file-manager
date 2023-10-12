import os
from typing import Optional, List

import click
import emoji
from directory_tree import display_tree

from app.logs.config import log_messages, logger_types
from app.utils.common import save_logs_to_file


@click.command()
@click.argument("dir_path", type=click.STRING)
@click.option(
    "--sort",
    type=click.Choice(["name", "size", "date", "modified", "type"], case_sensitive=False),
    default="name",
    show_default=True,
    help="Sorting criteria.",
)
@click.option(
    "--desc",
    is_flag=True,
    help="Display result in descending order.",
)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file.",
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

    dir_list = os.listdir(dir_path)
    files_list = [entry for entry in dir_list if os.path.isfile(os.path.join(dir_path, entry))]

    if not files_list:
        message = log_messages.NO_FILES.format(dir_path=dir_path)
    else:
        _sort_entries_list(dir_path, files_list, sort, desc)
        message = log_messages.LISTED_FILES.format(
            dir_path=dir_path, files_list="\n".join(files_list)
        )
    click.echo(message)
    if save:
        save_logs_to_file(output, dir_path, message, logger_types.BASIC)


@click.command()
@click.argument("dir_path", type=click.STRING)
@click.option(
    "--sort",
    type=click.Choice(["name", "size", "date", "modified"], case_sensitive=False),
    default="name",
    show_default=True,
    help="Sorting criteria.",
)
@click.option(
    "--desc",
    is_flag=True,
    help="Display result in descending order.",
)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file.",
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

    dir_list = os.listdir(dir_path)
    subdir_list = [entry for entry in dir_list if os.path.isdir(os.path.join(dir_path, entry))]

    if not subdir_list:
        message = log_messages.NO_SUBDIRS.format(dir_path=dir_path)
    else:
        _sort_entries_list(dir_path, subdir_list, sort, desc)
        message = log_messages.NESTED_SUBDIRS.format(
            dir_path=dir_path, subdir_list="\n".join(subdir_list)
        )
    click.echo(message)
    if save:
        save_logs_to_file(output, dir_path, message, logger_types.BASIC)


def _sort_entries_list(dir_path: str, entries_list: List[str], criteria: str, desc: bool) -> None:
    match criteria:
        case "name":
            sort_func = None
        case "size":
            sort_func = lambda file: os.path.getsize(os.path.join(dir_path, file))
        case "date":
            sort_func = lambda file: os.path.getctime(os.path.join(dir_path, file))
        case "modified":
            sort_func = lambda file: os.path.getmtime(os.path.join(dir_path, file))
        case "type":
            sort_func = lambda file: os.path.splitext(os.path.join(dir_path, file))[1]
        case _:
            sort_func = None
    entries_list.sort(key=sort_func, reverse=desc)


#############################################################
@click.command()
@click.argument("dir_path", type=click.STRING)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file.",
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

    dir_list = os.listdir(dir_path)
    files_list = []
    nested_dirs = []
    for entry in dir_list:
        if os.path.isfile(os.path.join(dir_path, entry)):
            files_list.append(entry)
        else:
            nested_dirs.append(entry)

    message = _get_catalog_messages(dir_path, files_list, nested_dirs)
    click.echo(message)
    if save:
        save_logs_to_file(output, dir_path, message, logger_types.CATALOG)


@click.command()
@click.argument("dir_path", type=click.STRING)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file.",
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

    message = _get_recursive_catalog(dir_path, None)
    click.echo(message)
    if save:
        save_logs_to_file(output, dir_path, message, logger_types.RECURSIVE)


def _get_recursive_catalog(root_dir: str, subdir_path: Optional[str]) -> str:
    if subdir_path is None:
        subdir_path = root_dir
    subdir_list = os.listdir(subdir_path)

    files_list = []
    nested_dirs = []
    inner_msg = ""
    for entry in subdir_list:
        entry_path = os.path.join(subdir_path, entry)
        if os.path.isfile(entry_path):
            files_list.append(entry)
        else:
            nested_dirs.append(entry)
            inner_msg += _get_recursive_catalog(root_dir, entry_path)

    message = _get_catalog_messages(subdir_path, files_list, nested_dirs)
    return message + inner_msg


def _get_catalog_messages(dir_path: str, files_list: List[str], nested_dirs: List[str]) -> str:
    if not files_list:
        files_msg = log_messages.NO_FILES.format(dir_path=dir_path)
    else:
        files_msg = log_messages.LISTED_FILES.format(
            dir_path=dir_path, files_list="\n".join(files_list)
        )

    if not nested_dirs:
        nested_dirs_msg = log_messages.NO_SUBDIRS.format(dir_path=dir_path)
    else:
        nested_dirs_msg = log_messages.NESTED_SUBDIRS.format(
            dir_path=dir_path, subdir_list="\n".join(nested_dirs)
        )
    return files_msg + nested_dirs_msg


#############################################################
@click.command()
@click.argument("dir_path", type=click.STRING)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file.",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def build_tree(dir_path: str, save: bool, output: str) -> None:
    """DIR_PATH: Path to directory to be scanned"""

    folder_emoji = emoji.emojize(":file_folder:")
    file_emoji = emoji.emojize(":page_with_curl:")

    tree_msg = ""
    for root, _, files in os.walk(dir_path):
        level = root.count(os.sep) - 1
        indent = " " * 4 * level
        tree_msg += "{}{} {}/\n".format(indent, folder_emoji, os.path.abspath(root))
        sub_indent = " " * 4 * (level + 1)
        for file in files:
            tree_msg += "{}{} {}\n".format(sub_indent, file_emoji, file)

    click.echo(tree_msg)
    if save:
        save_logs_to_file(output, dir_path, tree_msg, logger_types.TREE)


@click.command()
@click.argument("dir_path", type=click.STRING)
@click.option(
    "-h",
    "--hidden",
    is_flag=True,
    help="Include hidden files and folders.",
)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file.",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def build_pretty_tree(dir_path: str, hidden: bool, save: bool, output: str) -> None:
    """DIR_PATH: Path to directory to be scanned"""

    tree_msg = display_tree(dir_path, string_rep=True, show_hidden=hidden)
    click.echo(tree_msg)
    if save:
        save_logs_to_file(output, dir_path, tree_msg, logger_types.TREE)


#############################################################
@click.command()
@click.argument("dir_path", type=click.STRING)
@click.argument("name", type=click.STRING)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file.",
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

    dir_list = os.listdir(dir_path)
    files_list = []
    nested_dirs = []
    for entry in dir_list:
        if name in entry:
            if os.path.isfile(os.path.join(dir_path, entry)):
                files_list.append(entry)
            else:
                nested_dirs.append(entry)

    if not files_list and not nested_dirs:
        log_msg = log_messages.NOT_FOUND
    else:
        log_msg = log_messages.FOUND_BY_NAME.format(dir_path=dir_path, keyword=name)
        if files_list:
            log_msg += log_messages.FOUND_FILES_BY_NAME.format(
                files_list="\n\t- ".join(files_list),
            )
        if nested_dirs:
            log_msg += log_messages.FOUND_DIRS_BY_NAME.format(
                subdir_list="\n\t- ".join(nested_dirs),
            )
    click.echo(log_msg)
    if save:
        save_logs_to_file(output, dir_path, log_msg, logger_types.SEARCH)


@click.command()
@click.argument("dir_path", type=click.STRING)
@click.argument("name", type=click.STRING)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file.",
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

    log_msg = _get_search_result(dir_path, None, name)
    if not log_msg:
        log_msg = log_messages.NOT_FOUND
    click.echo(log_msg)
    if save:
        save_logs_to_file(output, dir_path, log_msg, logger_types.SEARCH)


def _get_search_result(root_dir: str, subdir_path: Optional[str], name: str) -> str:
    if subdir_path is None:
        subdir_path = root_dir
    subdir_list = os.listdir(subdir_path)

    files_list = []
    nested_dirs = []
    valid_dirs = []
    inner_msg = ""
    for entry in subdir_list:
        entry_path = os.path.join(subdir_path, entry)
        if os.path.isfile(entry_path) and name in entry:
            files_list.append(entry)
        elif os.path.isdir(entry_path):
            if name in entry:
                valid_dirs.append(entry)
            nested_dirs.append(entry)
            inner_msg += _get_search_result(root_dir, entry_path, name)

    if not files_list and not valid_dirs:
        return ""
    log_msg = log_messages.FOUND_BY_NAME.format(dir_path=subdir_path, keyword=name)
    if files_list:
        log_msg += log_messages.FOUND_FILES_BY_NAME.format(
            files_list="\n\t- ".join(files_list),
        )
    if valid_dirs:
        log_msg += log_messages.FOUND_DIRS_BY_NAME.format(
            subdir_list="\n\t- ".join(valid_dirs),
        )
    return log_msg + log_messages.DELIMITER + inner_msg
