import os
from os import path, listdir
from filecmp import dircmp
from logging import Logger

from directory_tree import display_tree

from manager.logs.config import log_messages, logger_types
from manager.logs.logger_factory import LoggerFactory


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
    logger = LoggerFactory.get_logger(logger_types.BASIC, output, save)

    dir_list = listdir(dir_path)
    os_func = getattr(path, os_func_name)
    entries_list = [entry for entry in dir_list if os_func(path.join(dir_path, entry))]
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
            sort_func = lambda file: path.getsize(path.join(dir_path, file))
        case "date":
            sort_func = lambda file: path.getctime(path.join(dir_path, file))
        case "modified":
            sort_func = lambda file: path.getmtime(path.join(dir_path, file))
        case "type":
            sort_func = lambda file: path.splitext(path.join(dir_path, file))[1]
        case _:
            sort_func = None
    entries_list.sort(key=sort_func, reverse=desc)


#############################################################
def build_catalog(
    dir_path: str,
    save: bool,
    output: str,
) -> None:
    logger = LoggerFactory.get_logger(logger_types.CATALOG, output, save)

    dir_list = listdir(dir_path)
    files_list = []
    nested_dirs = []
    for entry in dir_list:
        if path.isfile(path.join(dir_path, entry)):
            files_list.append(entry)
        else:
            nested_dirs.append(entry)
    logger.info(_get_catalog_messages(dir_path, files_list, nested_dirs))


def build_catalog_recursively(
    dir_path: str,
    save: bool,
    output: str,
) -> None:
    logger = LoggerFactory.get_logger(logger_types.RECURSIVE, output, save)
    logger.info(_get_recursive_catalog(logger, dir_path))


def _get_recursive_catalog(logger: Logger, root_dir: str, subdir_path: str | None = None) -> str:
    if subdir_path is None:
        subdir_path = root_dir
    subdir_list = listdir(subdir_path)

    files_list = []
    nested_dirs = []
    inner_msg = ""
    for entry in subdir_list:
        entry_path = path.join(subdir_path, entry)
        if path.isfile(entry_path):
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
    logger = LoggerFactory.get_logger(logger_types.TREE, output, save)

    folder_emoji = "\U0001f4c1"
    file_emoji = "\U0001f4c3"
    for root, dirs, files in os.walk(dir_path):
        if not show_hidden and path.basename(root).startswith("."):
            continue
        level = root.count(os.sep) - 1
        indent = " " * 4 * level
        logger.info(f"{indent}{folder_emoji} {path.abspath(root)}/")
        sub_indent = " " * 4 * (level + 1)
        for file in files:
            if not show_hidden and file.startswith("."):
                continue
            logger.info(f"{sub_indent}{file_emoji} {file}")


def build_pretty_tree(dir_path: str, show_hidden: bool, save: bool, output: str) -> None:
    logger = LoggerFactory.get_logger(logger_types.TREE, output, save)
    # TODO: be a man and implement form scratch!
    logger.info(display_tree(dir_path, string_rep=True, show_hidden=show_hidden))


#############################################################
def search_by_name(dir_path: str, name: str, save: bool, output: str) -> None:
    logger = LoggerFactory.get_logger(logger_types.ORGANIZE, output, save)

    dir_list = listdir(dir_path)
    files_list = []
    nested_dirs = []
    for entry in dir_list:
        if name in entry:
            if path.isfile(path.join(dir_path, entry)):
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
    logger = LoggerFactory.get_logger(logger_types.SEARCH, output, save)
    result_msg = _search_recursively(logger, root_dir, name, subdir_path)
    logger.info(result_msg or log_messages.NOT_FOUND)


def _search_recursively(logger: Logger, root_dir: str, name: str, subdir_path: str | None = None) -> str:
    if subdir_path is None:
        subdir_path = root_dir
    subdir_list = listdir(subdir_path)

    files_list = []
    nested_dirs = []
    valid_dirs = []
    inner_msg = ""
    for entry in subdir_list:
        entry_path = path.join(subdir_path, entry)
        if path.isfile(entry_path) and name in entry:
            files_list.append(entry)
        elif path.isdir(entry_path):
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
    save: bool,
    output: str,
    diff_recursively=False,
) -> None:
    logger = LoggerFactory.get_logger(logger_types.COMPARE, output, save)
    cmp_obj = dircmp(dir_path, other_path)
    diff_report(cmp_obj, include_hidden, diff_recursively, short, one_line, logger)


def diff_report(
    cmp_obj: dircmp,
    include_hidden: bool,
    diff_recursively: bool,
    short: bool,
    one_line: bool,
    logger: Logger,
) -> None:
    _report(cmp_obj, short, one_line, logger)

    if diff_recursively:
        for sub_dir in cmp_obj.subdirs.values():
            diff_report(sub_dir, include_hidden, diff_recursively, short, one_line, logger)


def _report(cmp_obj: dircmp, short: bool, one_line: bool, logger: Logger) -> None:
    # customizing dircmp.report()
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

    # if cmp_obj.left_only:
    #     cmp_obj.left_only.sort()
    #     logger.info(
    #         log_messages.DIFF_STATS.format(
    #             dir=cmp_obj.left, delimiter=delimiter, list=func(cmp_obj.left_only)
    #         )
    #     )
    # if cmp_obj.right_only:
    #     cmp_obj.right_only.sort()
    #     logger.info(
    #         log_messages.DIFF_STATS.format(
    #             dir=cmp_obj.right, delimiter=delimiter, list=func(cmp_obj.right_only)
    #         )
    #     )

    stats_messages ={
       'left_only':  log_messages.DIFF_STATS,
        'right_only': log_messages.DIFF_STATS,
        'same_files': log_messages.SAME_FILES,
        'diff_files': log_messages.DIFF_FILES,
        'funny_files': log_messages.TROUBLE_FILES,
        'common_dirs': log_messages.COMMON_SUBDIRS,
        'common_funny': log_messages.COMMON_TROUBLE,
    }

    for attr in ['left_only', 'right_only', 'same_files', 'diff_files', 'funny_files', 'common_dirs', 'common_funny']:
        if stats:= getattr(cmp_obj, attr, None):
            if attr=="left_only":
                dir_path = cmp_obj.left
            elif attr=="right_only":
                dir_path= cmp_obj.right
            else:
                dir_path= None
            _handle_stats_entries(dir_path, stats, logger, stats_messages[attr], delimiter, func)

    # if cmp_obj.same_files:
    #     cmp_obj.same_files.sort()
    #     logger.info(log_messages.SAME_FILES.format(delimiter=delimiter, list=func(cmp_obj.same_files)))
    # if cmp_obj.diff_files:
    #     cmp_obj.diff_files.sort()
    #     logger.info(log_messages.DIFF_FILES.format(delimiter=delimiter, list=func(cmp_obj.diff_files)))
    # if cmp_obj.funny_files:
    #     cmp_obj.funny_files.sort()
    #     logger.info(log_messages.TROUBLE_FILES.format(delimiter=delimiter, list=func(cmp_obj.funny_files)))
    # if cmp_obj.common_dirs:
    #     cmp_obj.common_dirs.sort()
    #     logger.info(log_messages.COMMON_SUBDIRS.format(delimiter=delimiter, list=func(cmp_obj.common_dirs)))
    # if cmp_obj.common_funny:
    #     cmp_obj.common_funny.sort()
    #     logger.info(log_messages.COMMON_TROUBLE.format(delimiter=delimiter, list=func(cmp_obj.common_funny)))

def _handle_stats_entries(dir_path, entries, logger, message, delimiter, func):
    fmt={
        'delimiter': delimiter,
        'list': func(entries)
    }
    if dir:
        fmt['dir'] = dir_path

    entries.sort()
    logger.info(message.format(**fmt))
