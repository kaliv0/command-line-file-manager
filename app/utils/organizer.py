import hashlib
import os
import shutil
from collections import defaultdict
from logging import Logger
from typing import List, Tuple

import click

from app.logs.config import log_messages, log_output, logger_types
from app.logs.logger_factory import LoggerFactory
from app.utils.config import constants


def organize_files(
    dir_path: str,
    exclude: str,
    hidden: bool,
    backup: bool,
    archive_format: str,
    save: bool,
    output: str,
) -> None:
    abs_dir_path, dir_list = _handle_dir_path(dir_path)
    logger = _configure_logger(dir_path, logger_types.ORGANIZE, output, save)
    _create_archive(abs_dir_path, archive_format, backup)

    exclude_list = exclude.split(",") if exclude else []
    for entry in dir_list:
        abs_entry_path = os.path.join(abs_dir_path, entry)
        if os.path.isfile(abs_entry_path):
            file_extension = os.path.splitext(entry)[1]
            if (not hidden and entry.startswith(".")) or file_extension in exclude_list:
                logger.info(log_messages.SKIP_FILE.format(entry=entry))
            else:
                _handle_entries(abs_dir_path, abs_entry_path, entry, file_extension, logger)


def organize_files_recursively(
    dir_path: str,
    exclude: str,
    exclude_dir: str,
    flat: bool,
    hidden: bool,
    backup: bool,
    archive_format: str,
    save: bool,
    output: str,
) -> None:
    abs_dir_path = os.path.abspath(dir_path)
    logger = _configure_logger(dir_path, logger_types.RECURSIVE_ORGANIZE, output, save)
    _create_archive(abs_dir_path, archive_format, backup)

    exclude_list = exclude.split(",") if exclude else []
    exclude_dir_list = exclude_dir.split(",") if exclude_dir else []
    if flat:
        root_dir = os.path.join(abs_dir_path, "")
        _handle_files_by_flattening_subdirs(
            abs_dir_path, "", root_dir, exclude_list, exclude_dir_list, hidden, logger
        )
    else:
        _handle_files(abs_dir_path, "", exclude_list, exclude_dir_list, hidden, logger)


def _handle_files(
    parent_dir: str,
    subdir_path: str,
    exclude_list: List[str],
    exclude_dir_list: List[str],
    hidden: bool,
    logger: Logger,
) -> None:
    abs_dir_path = os.path.join(parent_dir, subdir_path)
    dir_list = os.listdir(abs_dir_path)

    logger.info(log_messages.INSIDE_DIR.format(abs_dir_path=abs_dir_path))
    nested_dirs = []
    for entry in dir_list:
        abs_entry_path = os.path.join(abs_dir_path, entry)
        # handle files
        if os.path.isfile(abs_entry_path):
            if (
                entry == log_output.RECURSIVE_ORGANIZE_BASE
                or entry in constants.SKIPPED_BACKUP_FILES
            ):
                continue
            file_extension = os.path.splitext(entry)[1]
            if not hidden and entry.startswith(".") or file_extension in exclude_list:
                logger.info(log_messages.SKIP_FILE.format(entry=entry))
            else:
                _handle_entries(abs_dir_path, abs_entry_path, entry, file_extension, logger)
        # list nested dirs
        elif os.path.isdir(abs_entry_path):
            if entry.startswith(".") or entry in exclude_dir_list:
                logger.info(log_messages.SKIP_DIR.format(entry=entry))
                continue
            nested_dirs.append(abs_entry_path)
    # dive recursively to handle nested dirs
    for nested_dir in nested_dirs:
        _handle_files(abs_dir_path, nested_dir, exclude_list, exclude_dir_list, hidden, logger)


def _handle_files_by_flattening_subdirs(
    parent_dir: str,
    subdir_path: str,
    root_dir: str,
    exclude_list: List[str],
    exclude_dir_list: List[str],
    hidden: bool,
    logger: Logger,
) -> None:
    abs_dir_path = os.path.join(parent_dir, subdir_path)
    dir_list = os.listdir(abs_dir_path)

    logger.info(log_messages.INSIDE_DIR.format(abs_dir_path=abs_dir_path))
    nested_dirs = []
    for entry in dir_list:
        abs_entry_path = os.path.join(abs_dir_path, entry)
        # handle files
        if os.path.isfile(abs_entry_path):
            if (
                entry == log_output.RECURSIVE_ORGANIZE_BASE
                or entry in constants.SKIPPED_BACKUP_FILES
            ):
                continue
            file_extension = os.path.splitext(entry)[1]
            if not hidden and entry.startswith(".") or file_extension in exclude_list:
                logger.info(log_messages.MOVE_FILE_TO_ROOT_DIR.format(entry=entry))
                shutil.move(abs_entry_path, os.path.join(root_dir, entry))
            else:
                _handle_entries(root_dir, abs_entry_path, entry, file_extension, logger)
        # list nested dirs
        elif os.path.isdir(abs_entry_path):
            if entry.startswith(".") or entry in exclude_dir_list:
                logger.info(log_messages.SKIP_DIR_AND_MOVE.format(entry=entry))
                shutil.move(abs_entry_path, os.path.join(root_dir, entry))
                continue
            nested_dirs.append(abs_entry_path)
    # dive recursively to handle nested dirs
    for nested_dir in nested_dirs:
        _handle_files_by_flattening_subdirs(
            abs_dir_path, nested_dir, root_dir, exclude_list, exclude_dir_list, hidden, logger
        )
    # flatten dir
    is_not_root_dir = abs_dir_path != root_dir
    is_not_one_level_nested_dir = not os.path.join(os.path.dirname(abs_dir_path), "") == root_dir
    is_not_target_dir = os.path.basename(subdir_path) not in constants.TARGET_MAP.values()
    if is_not_root_dir and (is_not_one_level_nested_dir or is_not_target_dir):
        logger.info(log_messages.REMOVE_DIR.format(abs_dir_path=abs_dir_path))
        os.rmdir(abs_dir_path)


#####################################
def handle_duplicate_files(
    dir_path: str,
    interactive: bool,
    hidden: bool,
    backup: bool,
    archive_format: str,
    save: bool,
    output: str,
) -> None:
    abs_dir_path, dir_list = _handle_dir_path(dir_path)
    logger = _configure_logger(dir_path, logger_types.ORGANIZE, output, save)
    _create_archive(abs_dir_path, archive_format, backup)

    content_map = _create_duplicate_map(abs_dir_path, dir_list, hidden, logger)
    duplicate_list = _transform_content_map(content_map)
    # display sorted map entries
    if not duplicate_list:
        logger.info(log_messages.NO_DUPLICATE_FILES.format(dir_path=dir_path))
        return
    display_list = _prepare_display_list(duplicate_list)
    logger.info(
        log_messages.LISTED_DUPLICATE_FILES.format(dir_path=abs_dir_path, display_list=display_list)
    )
    # clean-up files
    _merge_duplicates(abs_dir_path, duplicate_list, interactive, logger)


def handle_duplicate_files_recursively(
    dir_path: str,
    interactive: bool,
    hidden: bool,
    save: bool,
    output: str,
    backup: bool,
    archive_format: str,
    logger: Logger,
) -> None:
    abs_dir_path, dir_list = _handle_dir_path(dir_path)
    if not logger:
        logger = _configure_logger(dir_path, logger_types.ORGANIZE, output, save)
    _create_archive(abs_dir_path, archive_format, backup)

    content_map, subdir_list = _create_duplicate_map_and_subdir_list(
        abs_dir_path, dir_list, hidden, logger
    )
    # ## handle duplicates in current dir ##
    logger.info(log_messages.INSIDE_DIR.format(abs_dir_path=abs_dir_path))
    duplicate_list = _transform_content_map(content_map)
    # display sorted map entries
    if not duplicate_list:
        logger.info(log_messages.NO_DUPLICATE_FILES_RECURSIVELY.format(dir_path=dir_path))
        return
    display_list = _prepare_display_list(duplicate_list)
    logger.info(
        log_messages.LISTED_DUPLICATE_FILES_RECURSIVELY.format(
            dir_path=abs_dir_path, display_list=display_list
        )
    )
    # clean-up files
    _merge_duplicates(abs_dir_path, duplicate_list, interactive, logger)
    # ## dive recursively into nested subdirs ##
    for subdir in subdir_list:
        handle_duplicate_files_recursively(
            subdir,
            interactive,
            hidden,
            save,
            output,
            backup=False,
            archive_format=None,
            logger=logger,
        )


def _create_duplicate_map(
    abs_dir_path: str, dir_list: str, hidden: bool, logger: Logger
) -> defaultdict[str, list[str]]:
    content_map = defaultdict(list[str])
    for entry in dir_list:
        abs_entry_path = os.path.join(abs_dir_path, entry)
        if os.path.isfile(abs_entry_path):
            if not hidden and entry.startswith("."):
                logger.info(log_messages.SKIP_FILE.format(entry=entry))
                continue

            with open(abs_entry_path, "rb") as f:
                sha = hashlib.sha1(f.read()).hexdigest()
            content_map[sha].append(entry)
    return content_map


def _create_duplicate_map_and_subdir_list(
    abs_dir_path: str, dir_list: str, hidden: bool, logger: Logger
) -> Tuple[defaultdict[str, list[str]], list[str]]:
    content_map = defaultdict(list[str])
    subdir_list = []
    for entry in dir_list:
        abs_entry_path = os.path.join(abs_dir_path, entry)
        if os.path.isfile(abs_entry_path):
            if not hidden and entry.startswith("."):
                logger.info(log_messages.SKIP_FILE.format(entry=entry))
                continue

            with open(abs_entry_path, "rb") as f:
                sha = hashlib.sha1(f.read()).hexdigest()
            content_map[sha].append(entry)
        elif os.path.isdir(abs_entry_path):
            subdir_list.append(abs_entry_path)
    return content_map, subdir_list


def _transform_content_map(content_map: defaultdict[str, list[str]]) -> list[list[str]]:
    return [sorted(file_list) for file_list in content_map.values() if len(file_list) > 1]


def _prepare_display_list(duplicate_list) -> str:
    display_list = ""
    for file_list in duplicate_list:
        for file in sorted(file_list):
            display_list += file + "\n"
        display_list += log_messages.DUPLICATE_DELIMITER
    return display_list


def _merge_duplicates(
    abs_dir_path: str, duplicate_list: list[list[str]], interactive: bool, logger: Logger
) -> None:
    for entry in duplicate_list:
        for idx, file in enumerate(entry):
            abs_file_path = os.path.join(abs_dir_path, file)
            if idx == 0:
                if interactive:
                    target_name = click.prompt(
                        text=log_messages.PRE_MERGE_PROMPT.format(entry=entry),
                        type=click.STRING,
                    )
                else:
                    target_name = file
                abs_target_path = os.path.join(abs_dir_path, target_name)
                logger.info(log_messages.MERGE_FILES.format(entry=entry, target_name=target_name))
                shutil.move(abs_file_path, abs_target_path)
            else:
                os.remove(abs_file_path)


# ### helpers ###
def _handle_dir_path(dir_path: str) -> Tuple[str, list[str]]:
    abs_dir_path = os.path.abspath(dir_path)
    dir_list = os.listdir(dir_path)
    return abs_dir_path, dir_list


def _configure_logger(dir_path: str, logger_type: str, output: str, save: bool) -> Logger:
    if not output:
        output = dir_path
    logger = LoggerFactory.get_logger(logger_type, output, save)
    return logger


def _create_archive(abs_dir_path: str, archive_format: str, backup: bool) -> None:
    if backup:
        shutil.make_archive(
            base_name=os.path.join(abs_dir_path, constants.BACKUP_FILE_NAME),
            format=archive_format,
            root_dir=os.path.dirname(abs_dir_path),
            base_dir=os.path.basename(abs_dir_path),
            verbose=True,
        )


def _handle_entries(
    abs_dir_path: str, abs_entry_path: str, entry: str, file_extension: str, logger: Logger
) -> None:
    if entry.startswith("."):
        target_dir_name = constants.TARGET_MAP["hidden"]
    else:
        target_dir_name = constants.TARGET_MAP.get(file_extension, constants.TARGET_MAP["default"])
    target_dir = os.path.join(abs_dir_path, target_dir_name)
    if not os.path.exists(target_dir):
        logger.info(log_messages.CREATE_FOLDER.format(target_dir=target_dir))
        os.makedirs(target_dir)
    logger.info(log_messages.MOVE_FILE.format(entry=entry, target_dir=target_dir))
    shutil.move(abs_entry_path, os.path.join(target_dir, entry))
