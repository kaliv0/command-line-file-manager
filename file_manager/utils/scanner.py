import os
from filecmp import dircmp
from logging import Logger
from typing import Callable

from directory_tree import display_tree

from file_manager.logs.config import log_messages, logger_types
from file_manager.logs.logger_factory import get_logger


def scan_files(dir_path: str, sort: str, desc: bool, save: bool, output: str) -> None:
    _scan_entries(dir_path, "isfile", sort, desc, save, output, "NO_FILES", "LISTED_FILES")


def scan_subdirs(dir_path: str, sort: str, desc: bool, save: bool, output: str) -> None:
    _scan_entries(dir_path, "isdir", sort, desc, save, output, "NO_SUBDIRS", "NESTED_SUBDIRS")


def _scan_entries(
    dir_path: str,
    os_func_name: str,
    sort: str,
    desc: bool,
    save: bool,
    output: str,
    not_found_msg: str,
    success_msg: str,
) -> None:
    logger = get_logger(logger_types.BASIC, output, save)

    dir_list = os.listdir(dir_path)
    os_func = getattr(os.path, os_func_name)
    entries_list = [entry for entry in dir_list if os_func(os.path.join(dir_path, entry))]
    if not entries_list:
        logger.info(getattr(log_messages, not_found_msg).format(dir_path=dir_path))
    else:
        _sort_entries_list(dir_path, entries_list, sort, desc)
        logger.info(
            getattr(log_messages, success_msg).format(
                dir_path=dir_path, entries_list="\n\t- ".join(entries_list)
            )
        )


def _sort_entries_list(dir_path: str, entries_list: list[str], criteria: str, desc: bool) -> None:
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
def build_catalog(
    dir_path: str,
    save: bool,
    output: str,
) -> None:
    logger = get_logger(logger_types.CATALOG, output, save)

    dir_list = os.listdir(dir_path)
    files_list = []
    nested_dirs = []
    for entry in dir_list:
        if os.path.isfile(os.path.join(dir_path, entry)):
            files_list.append(entry)
        else:
            nested_dirs.append(entry)
    logger.info(_get_catalog_messages(dir_path, files_list, nested_dirs))


def build_catalog_recursively(
    dir_path: str,
    save: bool,
    output: str,
) -> None:
    logger = get_logger(logger_types.RECURSIVE, output, save)
    logger.info(_get_recursive_catalog(logger, dir_path))


def _get_recursive_catalog(logger: Logger, root_dir: str, subdir_path: str | None = None) -> str:
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
            inner_msg += _get_recursive_catalog(logger, root_dir, entry_path)

    message = _get_catalog_messages(subdir_path, files_list, nested_dirs)
    return message + inner_msg


def _get_catalog_messages(dir_path: str, files_list: list[str], nested_dirs: list[str]) -> str:
    if not files_list:
        files_msg = log_messages.NO_FILES.format(dir_path=dir_path)
    else:
        files_msg = log_messages.LISTED_FILES.format(
            dir_path=dir_path, entries_list="\n\t- ".join(files_list)
        )

    if not nested_dirs:
        nested_dirs_msg = log_messages.NO_SUBDIRS.format(dir_path=dir_path)
    else:
        nested_dirs_msg = log_messages.NESTED_SUBDIRS.format(
            dir_path=dir_path, entries_list="\n\t- ".join(nested_dirs)
        )
    return files_msg + nested_dirs_msg


#############################################################
def build_tree(dir_path: str, show_hidden: bool, save: bool, output: str) -> None:
    logger = get_logger(logger_types.TREE, output, save)

    folder_emoji = "\U0001f4c1"
    file_emoji = "\U0001f4c3"
    for root, dirs, files in os.walk(dir_path):
        if not show_hidden and os.path.basename(root).startswith("."):
            continue
        level = root.count(os.sep) - 1
        indent = " " * 4 * level
        logger.info(f"{indent}{folder_emoji} {os.path.abspath(root)}/")
        sub_indent = " " * 4 * (level + 1)
        for file in files:
            if not show_hidden and file.startswith("."):
                continue
            logger.info(f"{sub_indent}{file_emoji} {file}")


def build_pretty_tree(dir_path: str, show_hidden: bool, save: bool, output: str) -> None:
    logger = get_logger(logger_types.TREE, output, save)
    logger.info(display_tree(dir_path, string_rep=True, show_hidden=show_hidden))


#############################################################
def search_by_name(dir_path: str, name: str, save: bool, output: str) -> None:
    logger = get_logger(logger_types.ORGANIZE, output, save)

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
        logger.info(log_messages.FOUND_BY_NAME.format(dir_path=dir_path, keyword=name, delimiter=""))
        if files_list:
            logger.info(
                log_messages.FOUND_FILES_BY_NAME.format(files_list="\n\t- ".join(files_list), delimiter="")
            )
        if nested_dirs:
            logger.info(
                log_messages.FOUND_DIRS_BY_NAME.format(subdir_list="\n\t- ".join(nested_dirs), delimiter="")
            )


def search_by_name_recursively(
    root_dir: str, name: str, save: bool, output: str, subdir_path: str | None = None
) -> None:
    logger = get_logger(logger_types.SEARCH, output, save)
    result_msg = _search_recursively(logger, root_dir, name, subdir_path)
    logger.info(result_msg or log_messages.NOT_FOUND)


def _search_recursively(logger: Logger, root_dir: str, name: str, subdir_path: str | None = None) -> str:
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


#############################################################
def compare_directories(
    dir_path: str,
    other_path: str,
    include_hidden: bool,
    short: bool,
    one_line: bool,
    recursively: bool,
    save: bool,
    output: str,
) -> None:
    abs_dir_path = os.path.abspath(dir_path)
    abs_other_path = os.path.abspath(other_path)
    if not include_hidden and any(
        os.path.basename(entry).startswith(".") for entry in (abs_dir_path, abs_other_path)
    ):
        return

    logger = get_logger(logger_types.COMPARE, output, save)
    cmp_obj = dircmp(abs_dir_path, abs_other_path)
    diff_report(cmp_obj, include_hidden, recursively, short, one_line, logger)


def diff_report(
    cmp_obj: dircmp,
    include_hidden: bool,
    diff_recursively: bool,
    short: bool,
    one_line: bool,
    logger: Logger,
) -> None:
    _report(cmp_obj, include_hidden, short, one_line, logger)

    if diff_recursively:
        for sub_dir in cmp_obj.subdirs.values():
            diff_report(sub_dir, include_hidden, diff_recursively, short, one_line, logger)


def _report(cmp_obj: dircmp, include_hidden: bool, short: bool, one_line: bool, logger: Logger) -> None:
    logger.info(log_messages.DIRS_DIFF.format(left=cmp_obj.left, right=cmp_obj.right))

    if short:
        delimiter = ": "
        func = lambda files: len(files)
    elif one_line:
        delimiter = ":\n\t"
        func = lambda files: files
    else:
        delimiter = ":\n\t- "
        func = lambda files: "\n\t- ".join(files)

    stats_map = {
        "left_only": log_messages.DIFF_STATS,
        "right_only": log_messages.DIFF_STATS,
        "same_files": log_messages.SAME_FILES,
        "diff_files": log_messages.DIFF_FILES,
        "funny_files": log_messages.TROUBLE_FILES,
        "common_dirs": log_messages.COMMON_SUBDIRS,
        "common_funny": log_messages.COMMON_TROUBLE,
    }

    for attr in stats_map.keys():
        if stats := getattr(cmp_obj, attr, None):
            if not include_hidden:
                if not (stats := [entry for entry in stats if not entry.startswith(".")]):
                    continue

            if attr == "left_only":
                dir_path = cmp_obj.left
            elif attr == "right_only":
                dir_path = cmp_obj.right
            else:
                dir_path = None
            _handle_stats_entries(dir_path, stats, logger, stats_map[attr], delimiter, func)


def _handle_stats_entries(
    dir_path: str,
    entries: list[str],
    logger: Logger,
    message: str,
    delimiter: str,
    func: Callable[[list[str]], str | int],
) -> None:
    fmt = {"delimiter": delimiter, "list": func(entries)}
    if dir:
        fmt["dir"] = dir_path

    entries.sort()
    logger.info(message.format(**fmt))
