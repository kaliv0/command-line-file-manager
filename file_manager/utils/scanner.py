import os
from collections.abc import Iterator
from filecmp import dircmp
import itertools
from logging import Logger
from typing import Callable

from file_manager.logs import log_messages
from file_manager.logs.logger_factory import get_logger


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


def show(dir_path: str, sort: str, desc: bool, list_dirs: bool, save: bool, output: str, log: str) -> None:
    if list_dirs:
        os_func_name = "isdir"
        not_found_msg = "NO_SUBDIRS"
        success_msg = "NESTED_SUBDIRS"
    else:
        os_func_name = "isfile"
        not_found_msg = "NO_FILES"
        success_msg = "LISTED_FILES"

    logger = get_logger(output, save, log)

    dir_list = os.listdir(dir_path)
    os_func = getattr(os.path, os_func_name)
    if entries_list := [entry for entry in dir_list if os_func(os.path.join(dir_path, entry))]:
        _sort_entries_list(dir_path, entries_list, sort, desc)
        logger.info(
            getattr(log_messages, success_msg).format(
                dir_path=os.path.abspath(dir_path), entries_list="\n\t- ".join(entries_list)
            )
        )
    else:
        logger.info(getattr(log_messages, not_found_msg).format(dir_path=os.path.abspath(dir_path)))


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
def scan(dir_path: str, sort: str, desc: bool, save: bool, output: str, log: str) -> None:
    logger = get_logger(output, save, log)

    dir_list = os.listdir(dir_path)
    files_list = []
    nested_dirs = []
    for entry in dir_list:
        if os.path.isfile(os.path.join(dir_path, entry)):
            files_list.append(entry)
        else:
            nested_dirs.append(entry)
    logger.info(_get_catalog_messages(dir_path, files_list, nested_dirs, sort, desc))


def scan_recursively(dir_path: str, sort: str, desc: bool, save: bool, output: str, log: str) -> None:
    logger = get_logger(output, save, log)
    logger.info("".join(_get_recursive_catalog(sort, desc, dir_path)))


def _get_recursive_catalog(
    sort: str, desc: bool, root_dir: str, subdir_path: str | None = None
) -> Iterator[str]:
    if subdir_path is None:
        subdir_path = root_dir

    files_list = []
    nested_dirs = []
    inner_log_gen = []
    subdir_list = os.listdir(subdir_path)
    for entry in subdir_list:
        entry_path = os.path.join(subdir_path, entry)
        if os.path.isfile(entry_path):
            files_list.append(entry)
        else:
            nested_dirs.append(entry)
            inner_log_gen.append(_get_recursive_catalog(sort, desc, root_dir, entry_path))
    yield _get_catalog_messages(subdir_path, files_list, nested_dirs, sort, desc)
    yield from itertools.chain(*inner_log_gen)


def _get_catalog_messages(
    dir_path: str, files_list: list[str], nested_dirs: list[str], sort: str, desc: bool
) -> str:
    if not files_list:
        files_msg = log_messages.NO_FILES.format(dir_path=os.path.abspath(dir_path))
    else:
        _sort_entries_list(dir_path, files_list, sort, desc)
        files_msg = log_messages.LISTED_FILES.format(
            dir_path=os.path.abspath(dir_path), entries_list="\n\t- ".join(files_list)
        )

    if not nested_dirs:
        nested_dirs_msg = log_messages.NO_SUBDIRS.format(dir_path=os.path.abspath(dir_path))
    else:
        _sort_entries_list(dir_path, nested_dirs, sort, desc)
        nested_dirs_msg = log_messages.NESTED_SUBDIRS.format(
            dir_path=os.path.abspath(dir_path), entries_list="\n\t- ".join(nested_dirs)
        )
    return files_msg + nested_dirs_msg


#############################################################
def build_tree(
    dir_path: str, max_depth: int, show_hidden: bool, dirs_only: bool, save: bool, output: str, log: str
) -> None:
    logger = get_logger(output, save, log)
    root_level = os.path.normpath(dir_path).count(os.sep)

    for curr_root, dirs, files in os.walk(dir_path):
        if not show_hidden and os.path.basename(curr_root).startswith("."):
            continue

        level = os.path.normpath(curr_root).count(os.sep) - root_level
        if max_depth is not None and level > max_depth:
            continue

        indent = " " * 4 * level
        logger.info(f"{indent}{FOLDER_EMOJI} {os.path.abspath(curr_root)}/")
        if not dirs_only:
            sub_indent = " " * 4 * (level + 1)
            _build_file_tree(files, show_hidden, sub_indent, logger)


def _build_file_tree(files: list[str], show_hidden: bool, sub_indent: str, logger: Logger) -> None:
    for file in files:
        if not show_hidden and file.startswith("."):
            continue
        logger.info(f"{sub_indent}{FILE_EMOJI} {file}")


#############################################################
def search(dir_path: str, name: str, save: bool, output: str, log: str) -> None:
    logger = get_logger(output, save, log)

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
        return

    logger.info(
        log_messages.FOUND_BY_NAME.format(dir_path=os.path.abspath(dir_path), keyword=name, delimiter="")
    )
    if files_list:
        logger.info(
            log_messages.FOUND_FILES_BY_NAME.format(files_list="\n\t- ".join(files_list), delimiter="")
        )
    if nested_dirs:
        logger.info(
            log_messages.FOUND_DIRS_BY_NAME.format(subdir_list="\n\t- ".join(nested_dirs), delimiter="")
        )


def search_recursively(
    root_dir: str, name: str, save: bool, output: str, log: str, subdir_path: str | None = None
) -> None:
    logger = get_logger(output, save, log)
    result_msg = "".join(_search_recursively(root_dir, name, subdir_path))
    logger.info(result_msg or log_messages.NOT_FOUND)


def _search_recursively(root_dir: str, name: str, subdir_path: str | None = None) -> Iterator[str]:
    if subdir_path is None:
        subdir_path = root_dir
    subdir_list = os.listdir(subdir_path)

    files_list = []
    nested_dirs = []
    valid_dirs = []
    inner_log_gen = []
    for entry in subdir_list:
        entry_path = os.path.join(subdir_path, entry)
        if os.path.isfile(entry_path) and name in entry:
            files_list.append(entry)
        elif os.path.isdir(entry_path):
            if name in entry:
                valid_dirs.append(entry)
            nested_dirs.append(entry)
            inner_log_gen.append(_search_recursively(root_dir, name, entry_path))

    if not files_list and not valid_dirs:
        yield from itertools.chain(*inner_log_gen)
        return

    log_msg = [
        log_messages.FOUND_BY_NAME.format(dir_path=os.path.abspath(subdir_path), keyword=name, delimiter="\n")
    ]
    if files_list:
        log_msg.append(
            log_messages.FOUND_FILES_BY_NAME.format(files_list="\n\t- ".join(files_list), delimiter="\n")
        )
    if valid_dirs:
        log_msg.append(
            log_messages.FOUND_DIRS_BY_NAME.format(subdir_list="\n\t- ".join(valid_dirs), delimiter="\n")
        )
    log_msg.append(log_messages.DELIMITER)
    yield "".join(log_msg)
    yield from itertools.chain(*inner_log_gen)


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
    log: str,
) -> None:
    logger = get_logger(output, save, log)

    abs_dir_path = os.path.abspath(dir_path)
    abs_other_path = os.path.abspath(other_path)
    if abs_dir_path == abs_other_path:
        logger.info(log_messages.IDENTICAL_PATHS)
        return

    if not include_hidden and any(
        os.path.basename(entry).startswith(".") for entry in (abs_dir_path, abs_other_path)
    ):
        return

    cmp_obj = dircmp(abs_dir_path, abs_other_path)
    _diff_report(cmp_obj, include_hidden, recursively, short, one_line, logger)


def _diff_report(
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
            _diff_report(sub_dir, include_hidden, diff_recursively, short, one_line, logger)


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

    for attr in STATS_MAP:
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
