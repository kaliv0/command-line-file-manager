import os
from logging import Logger

import emoji
from directory_tree import display_tree

from manager.logs.config import log_messages, logger_types
from manager.logs.logger_factory import LoggerFactory


# TODO: move as private function underneath
def sort_entries_list(dir_path: str, entries_list: list[str], criteria: str, desc: bool) -> None:
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


# TODO: scan_files and scan_subdirs can be combined -> 90% similar
def scan_files(dir_path: str, sort: str, desc: bool, save: bool, output: str) -> None:
    logger = LoggerFactory.get_logger(dir_path, logger_types.BASIC, output, save)

    dir_list = os.listdir(dir_path)
    files_list = [entry for entry in dir_list if os.path.isfile(os.path.join(dir_path, entry))]
    if not files_list:
        logger.info(log_messages.NO_FILES.format(dir_path=dir_path))
    else:
        sort_entries_list(dir_path, files_list, sort, desc)
        logger.info(
            log_messages.LISTED_FILES.format(dir_path=dir_path, files_list="\n".join(files_list))
        )


def scan_subdirs(
    dir_path: str,
    sort: str,
    desc: bool,
    save: bool,
    output: str,
) -> None:
    logger = LoggerFactory.get_logger(dir_path, logger_types.BASIC, output, save)

    dir_list = os.listdir(dir_path)
    subdir_list = [entry for entry in dir_list if os.path.isdir(os.path.join(dir_path, entry))]
    if not subdir_list:
        logger.info(log_messages.NO_SUBDIRS.format(dir_path=dir_path))
    else:
        sort_entries_list(dir_path, subdir_list, sort, desc)
        logger.info(
            log_messages.NESTED_SUBDIRS.format(
                dir_path=dir_path, subdir_list="\n".join(subdir_list)
            )
        )


#############################################################
def build_catalog(dir_path: str) -> str:
    dir_list = os.listdir(dir_path)
    files_list = []
    nested_dirs = []
    for entry in dir_list:
        if os.path.isfile(os.path.join(dir_path, entry)):
            files_list.append(entry)
        else:
            nested_dirs.append(entry)
    return _get_catalog_messages(dir_path, files_list, nested_dirs)


def get_recursive_catalog(root_dir: str, subdir_path: str | None = None) -> str:
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
            inner_msg += get_recursive_catalog(root_dir, entry_path)

    message = _get_catalog_messages(subdir_path, files_list, nested_dirs)
    return message + inner_msg


def _get_catalog_messages(dir_path: str, files_list: list[str], nested_dirs: list[str]) -> str:
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
def build_tree(dir_path: str, show_hidden: bool, save: bool, output: str) -> None:
    logger = LoggerFactory.get_logger(dir_path, logger_types.TREE, output, save)

    folder_emoji = emoji.emojize(":file_folder:")  # TODO: put inline
    file_emoji = emoji.emojize(":page_with_curl:")

    for root, dirs, files in os.walk(dir_path):
        if not show_hidden and os.path.basename(root).startswith("."):
            continue
        level = root.count(os.sep) - 1
        indent = " " * 4 * level
        # TODO: refactor formatting -> inside {}
        #  check if we need extra new_line at the end??
        logger.info("{}{} {}/\n".format(indent, folder_emoji, os.path.abspath(root)))
        sub_indent = " " * 4 * (level + 1)
        for file in files:
            if not show_hidden and file.startswith("."):
                continue
            logger.info("{}{} {}\n".format(sub_indent, file_emoji, file))


def build_pretty_tree(dir_path: str, show_hidden: bool, save: bool, output: str) -> None:
    logger = LoggerFactory.get_logger(dir_path, logger_types.TREE, output, save)
    # TODO: be a man and implement form scratch!
    logger.info(display_tree(dir_path, string_rep=True, show_hidden=show_hidden))


#############################################################
def search_by_name(dir_path: str, name: str, save: bool, output: str) -> None:
    logger = LoggerFactory.get_logger(dir_path, logger_types.ORGANIZE, output, save)

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
        logger.info(log_messages.NOT_FOUND)
    else:
        logger.info(
            log_messages.FOUND_BY_NAME.format(dir_path=dir_path, keyword=name, delimiter="")
        )
        if files_list:
            logger.info(
                log_messages.FOUND_FILES_BY_NAME.format(
                    files_list="\n\t- ".join(files_list), delimiter=""
                )
            )
        if nested_dirs:
            logger.info(
                log_messages.FOUND_DIRS_BY_NAME.format(
                    subdir_list="\n\t- ".join(nested_dirs), delimiter=""
                )
            )


def search_by_name_recursively(
    root_dir: str, name: str, save: bool, output: str, subdir_path: str | None = None
) -> None:
    logger = LoggerFactory.get_logger(root_dir, logger_types.SEARCH, output, save)
    logger.info(_search_recursively(logger, root_dir, name, subdir_path))


def _search_recursively(
    logger: Logger, root_dir: str, name: str, subdir_path: str | None = None
) -> str:
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
            inner_msg += _search_recursively(logger, root_dir, name, entry_path)

    if not files_list and not valid_dirs:
        return ""
    log_msg = log_messages.FOUND_BY_NAME.format(dir_path=subdir_path, keyword=name, delimiter="\n")
    if files_list:
        log_msg += log_messages.FOUND_FILES_BY_NAME.format(
            files_list="\n\t- ".join(files_list), delimiter="\n"
        )
    if valid_dirs:
        log_msg += log_messages.FOUND_DIRS_BY_NAME.format(
            subdir_list="\n\t- ".join(valid_dirs), delimiter="\n"
        )
    return log_msg + log_messages.DELIMITER + inner_msg
