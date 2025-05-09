import os
import re
from collections.abc import Generator
from filecmp import dircmp
from logging import Logger
from typing import Callable

from file_manager.logs import log_messages
from file_manager.logs.logger_factory import get_logger
from file_manager.utils import should_skip_hidden

FOLDER_EMOJI = "\U0001f4c1"
FILE_EMOJI = "\U0001f4c3"
STATS_MAP = {
    "left_only": log_messages.DIFF_STATS,
    "right_only": log_messages.DIFF_STATS,
    "same_files": log_messages.SAME_FILES,
    "diff_files": log_messages.DIFF_FILES,
    "funny_files": log_messages.TROUBLE_FILES,
    "common_dirs": log_messages.COMMON_SUBDIRS,
    "common_funny": log_messages.COMMON_TROUBLE,
}
DIR_SHOW_MAP = {
    "os_func_name": "isdir",
    "not_found_msg": "NO_SUBDIRS",
    "success_msg": "NESTED_SUBDIRS",
}
FILE_SHOW_MAP = {
    "os_func_name": "isfile",
    "not_found_msg": "NO_FILES",
    "success_msg": "LISTED_FILES",
}


def show(
    dir_path: str,
    show_hidden: bool,
    sort: str,
    desc: bool,
    list_dirs: bool,
    save: bool,
    output: str,
    log: str,
) -> None:
    show_map = DIR_SHOW_MAP if list_dirs else FILE_SHOW_MAP
    logger = get_logger(output, save, log)

    dir_list = os.listdir(dir_path)
    if entries := _build_entries_list(dir_path, dir_list, show_map["os_func_name"], show_hidden):
        _sort_entries_list(dir_path, entries, sort, desc)
        logger.info(
            getattr(log_messages, show_map["success_msg"]).format(
                dir_path=os.path.abspath(dir_path),
                entries_list=_format_entries(entries),
            )
        )
    else:
        logger.info(
            getattr(log_messages, show_map["not_found_msg"]).format(dir_path=os.path.abspath(dir_path))
        )


def _build_entries_list(
    dir_path: str, dir_list: list[str], os_func_name: str, show_hidden: bool
) -> list[str]:
    os_func = getattr(os.path, os_func_name)
    entries_list = []
    for entry in dir_list:
        if not os_func(os.path.join(dir_path, entry)) or should_skip_hidden(show_hidden, entry):
            continue
        entries_list.append(entry)
    return entries_list


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
def scan(dir_path: str, show_hidden: bool, sort: str, desc: bool, save: bool, output: str, log: str) -> None:
    logger = get_logger(output, save, log)

    dir_list = os.listdir(dir_path)
    files_list = []
    nested_dirs = []
    for entry in dir_list:
        if should_skip_hidden(show_hidden, entry):
            continue
        if os.path.isfile(os.path.join(dir_path, entry)):
            files_list.append(entry)
        else:
            nested_dirs.append(entry)

    for log_msg in _get_catalog_messages(dir_path, files_list, nested_dirs, sort, desc):
        logger.info(log_msg)


def scan_recursively(
    dir_path: str, show_hidden: bool, sort: str, desc: bool, save: bool, output: str, log: str
) -> None:
    logger = get_logger(output, save, log)
    for log_msg in _get_recursive_catalog(show_hidden, sort, desc, dir_path):
        logger.info(log_msg)


def _get_recursive_catalog(
    show_hidden: bool, sort: str, desc: bool, root_dir: str, subdir_path: str | None = None
) -> Generator[str]:
    if subdir_path is None:
        subdir_path = root_dir

    files_list = []
    nested_dirs = []
    subdir_list = os.listdir(subdir_path)
    for entry in subdir_list:
        if should_skip_hidden(show_hidden, entry):
            continue
        entry_path = os.path.join(subdir_path, entry)
        if os.path.isfile(entry_path):
            files_list.append(entry)
        else:
            nested_dirs.append(entry)

    yield from _get_catalog_messages(subdir_path, files_list, nested_dirs, sort, desc)
    for entry in nested_dirs:
        yield from _get_recursive_catalog(show_hidden, sort, desc, root_dir, os.path.join(subdir_path, entry))


def _get_catalog_messages(
    dir_path: str, files_list: list[str], nested_dirs: list[str], sort: str, desc: bool
) -> tuple[str, str]:
    if not files_list:
        files_msg = log_messages.NO_FILES.format(dir_path=os.path.abspath(dir_path))
    else:
        _sort_entries_list(dir_path, files_list, sort, desc)
        files_msg = log_messages.LISTED_FILES.format(
            dir_path=os.path.abspath(dir_path), entries_list=_format_entries(files_list)
        )

    if not nested_dirs:
        nested_dirs_msg = log_messages.NO_SUBDIRS.format(dir_path=os.path.abspath(dir_path))
    else:
        _sort_entries_list(dir_path, nested_dirs, sort, desc)
        nested_dirs_msg = log_messages.NESTED_SUBDIRS.format(
            dir_path=os.path.abspath(dir_path), entries_list=_format_entries(nested_dirs)
        )
    return files_msg, nested_dirs_msg


#############################################################
def build_tree(
    dir_path: str,
    max_depth: int,
    show_hidden: bool,
    dirs_only: bool,
    save: bool,
    output: str,
    log: str,
) -> None:
    logger = get_logger(output, save, log)
    root_level = os.path.normpath(dir_path).count(os.sep)
    if max_depth is None:
        max_depth = 20

    for curr_root, dirs, files in os.walk(dir_path):
        if should_skip_hidden(show_hidden, os.path.basename(curr_root)):
            continue

        level = os.path.normpath(curr_root).count(os.sep) - root_level
        if level > max_depth + 1:
            continue

        indent = " " * 4 * level
        logger.info(f"{indent}{FOLDER_EMOJI} {os.path.abspath(curr_root)}/\n")
        # NB: we print subdirs from the next level (max_depth + 1) but not the files inside them ( level <= max_depth)
        if not dirs_only and level <= max_depth:
            sub_indent = " " * 4 * (level + 1)
            _build_file_tree(files, show_hidden, sub_indent, logger)


def _build_file_tree(files: list[str], show_hidden: bool, sub_indent: str, logger: Logger) -> None:
    for file in files:
        if should_skip_hidden(show_hidden, file):
            continue
        logger.info(f"{sub_indent}{FILE_EMOJI} {file}\n")


#############################################################
def search(dir_path: str, name: str, use_regex: bool, save: bool, output: str, log: str) -> None:
    logger = get_logger(output, save, log)

    dir_list = os.listdir(dir_path)
    files_list = []
    nested_dirs = []
    for entry in dir_list:
        if _search_in_entry_name(name, entry, use_regex):
            if os.path.isfile(os.path.join(dir_path, entry)):
                files_list.append(entry)
            else:
                nested_dirs.append(entry)

    if not files_list and not nested_dirs:
        logger.info(log_messages.NOT_FOUND)
        return

    logger.info(log_messages.FOUND_BY_NAME.format(dir_path=os.path.abspath(dir_path), keyword=name))
    if files_list:
        logger.info(log_messages.FOUND_FILES_BY_NAME.format(files_list=_format_entries(files_list)))
    if nested_dirs:
        logger.info(log_messages.FOUND_DIRS_BY_NAME.format(subdir_list=_format_entries(nested_dirs)))


def search_recursively(
    root_dir: str,
    name: str,
    use_regex: bool,
    save: bool,
    output: str,
    log: str,
    subdir_path: str | None = None,
) -> None:
    logger = get_logger(output, save, log)
    log_gen = _search_recursively(root_dir, name, use_regex, subdir_path)
    if not (log_msg := next(log_gen, None)):
        logger.info(log_messages.NOT_FOUND)
    else:
        logger.info(log_msg)
        for rest_msg in log_gen:
            logger.info(rest_msg)


def _search_recursively(
    root_dir: str, name: str, use_regex: bool, subdir_path: str | None = None
) -> Generator[str]:
    if subdir_path is None:
        subdir_path = root_dir
    subdir_list = os.listdir(subdir_path)

    files_list = []
    nested_dirs = []
    valid_dirs = []
    for entry in subdir_list:
        entry_path = os.path.join(subdir_path, entry)
        if os.path.isfile(entry_path) and _search_in_entry_name(name, entry, use_regex):
            files_list.append(entry)
        elif os.path.isdir(entry_path):
            if _search_in_entry_name(name, entry, use_regex):
                valid_dirs.append(entry)
            nested_dirs.append(entry)

    log_msg = []
    if files_list or valid_dirs:
        curr_log = log_messages.FOUND_BY_PATTERN if use_regex else log_messages.FOUND_BY_NAME
        log_msg.append(curr_log.format(dir_path=os.path.abspath(subdir_path), sequence=name))
        if files_list:
            log_msg.append(log_messages.FOUND_FILES_BY_NAME.format(files_list=_format_entries(files_list)))
        if valid_dirs:
            log_msg.append(log_messages.FOUND_DIRS_BY_NAME.format(subdir_list=_format_entries(valid_dirs)))
        log_msg.append(log_messages.DELIMITER)

    yield from log_msg
    for entry in nested_dirs:
        yield from _search_recursively(root_dir, name, use_regex, os.path.join(subdir_path, entry))


def _search_in_entry_name(name: str, entry: str, use_regex: bool):
    if use_regex:
        return re.search(name, entry)
    return name in entry


#############################################################
def compare_directories(
    dir_path: str,
    other_path: str,
    ignore: str,
    show_hidden: bool,
    short: bool,
    one_line: bool,
    recursively: bool,
    save: bool,
    output: str,
    log: str,
) -> None:
    logger = get_logger(output, save, log)

    abs_dir_path = os.path.abspath(dir_path)
    abs_other_path = os.path.abspath(other_path)
    if abs_dir_path == abs_other_path:
        logger.info(log_messages.IDENTICAL_PATHS)
        return

    if should_skip_hidden(show_hidden, abs_dir_path, abs_other_path):
        return

    ignore_list = ignore.split(",") if ignore else []
    cmp_obj = dircmp(abs_dir_path, abs_other_path, ignore=ignore_list)
    _diff_report(cmp_obj, show_hidden, recursively, short, one_line, logger)


def _diff_report(
    cmp_obj: dircmp,
    show_hidden: bool,
    diff_recursively: bool,
    short: bool,
    one_line: bool,
    logger: Logger,
) -> None:
    _report(cmp_obj, show_hidden, short, one_line, logger)

    if diff_recursively:
        for sub_dir in cmp_obj.subdirs.values():
            if should_skip_hidden(show_hidden, sub_dir.left, sub_dir.right):
                continue
            _diff_report(sub_dir, show_hidden, diff_recursively, short, one_line, logger)


def _report(cmp_obj: dircmp, show_hidden: bool, short: bool, one_line: bool, logger: Logger) -> None:
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

    for attr in STATS_MAP:
        if not (stats := getattr(cmp_obj, attr, None)):
            continue
        if not show_hidden:
            # recompute stats to exclude hidden entries
            stats = [entry for entry in stats if not entry.startswith(".")]
            if not stats:
                continue

        if attr == "left_only":
            dir_path = cmp_obj.left
        elif attr == "right_only":
            dir_path = cmp_obj.right
        else:
            dir_path = None
        _handle_stats_entries(dir_path, stats, logger, STATS_MAP[attr], delimiter, func)


def _handle_stats_entries(
    dir_path: str,
    entries: list[str],
    logger: Logger,
    message: str,
    delimiter: str,
    func: Callable[[list[str]], str | int],
) -> None:
    fmt = {"delimiter": delimiter, "list": func(entries)}
    if dir_path:
        fmt["dir"] = dir_path

    entries.sort()
    logger.info(message.format(**fmt))


# ### helpers ###
def _format_entries(entries: list[str]) -> str:
    return "\n\t- ".join(entries)
