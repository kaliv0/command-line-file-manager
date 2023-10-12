import logging
import os
import shutil
from typing import List

import click

import app.utils.config.constants
from app.logs.config import log_messages, logger_types, log_output
from app.logs.logger_factory import LoggerFactory
from app.utils.config.constants import TARGET_MAP


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
    "-h",
    "--hidden",
    is_flag=True,
    help="Include hidden files.",
)
@click.option(
    "-b",
    "--backup",
    is_flag=True,
    help="Create an archived file of the given directory before re-organizing it.",
)
@click.option(
    "-f",
    "--archive-format",
    type=click.Choice(["tar", "zip"], case_sensitive=False),
    default=None,
    show_default=True,
    help="Archive format for backup file.",
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
def organize_files(
    dir_path: str,
    exclude: str,
    hidden: bool,
    backup: bool,
    archive_format: str,
    save: bool,
    output: str,
) -> None:
    """
    Search recursively by NAME inside DIR_PATH
    """

    exclude_list = exclude.split(",") if exclude else []

    dir_list = os.listdir(dir_path)
    abs_dir_path = os.path.abspath(dir_path)

    if not output:
        output = dir_path
    logger = LoggerFactory.get_logger(logger_types.ORGANIZE, output, save)

    if backup:
        shutil.make_archive(
            base_name=os.path.join(abs_dir_path, app.utils.config.constants.BACKUP_FILE_NAME),
            format=archive_format,
            root_dir=os.path.dirname(abs_dir_path),
            base_dir=os.path.basename(abs_dir_path),
            verbose=True,
        )

    for entry in dir_list:
        abs_entry_path = os.path.join(abs_dir_path, entry)
        if os.path.isfile(abs_entry_path):
            file_extension = os.path.splitext(entry)[1]
            if (not hidden and entry.startswith(".")) or file_extension in exclude_list:
                logger.info(log_messages.SKIP_FILE.format(entry=entry))
                continue

            if entry.startswith("."):
                target_dir_name = TARGET_MAP["hidden"]
            else:
                target_dir_name = TARGET_MAP.get(file_extension, TARGET_MAP["default"])

            target_dir = os.path.join(abs_dir_path, target_dir_name)
            if not os.path.exists(target_dir):
                logger.info(log_messages.CREATE_FOLDER.format(target_dir=target_dir))
                os.makedirs(target_dir)
            logger.info(log_messages.MOVE_FILE.format(entry=entry, target_dir=target_dir))
            shutil.move(abs_entry_path, os.path.join(target_dir, entry))


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
    help="Move all files to target directories inside parent folder.",
)
@click.option(
    "-h",
    "--hidden",
    is_flag=True,
    help="Include hidden files and folders.",
)
@click.option(
    "-b",
    "--backup",
    is_flag=True,
    help="Create an archived file of the given directory before re-organizing it.",
)
@click.option(
    "-f",
    "--archive-format",
    type=click.Choice(["tar", "zip"], case_sensitive=False),
    default=None,
    show_default=True,
    help="Archive format for backup file.",
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
    """
    Search recursively by NAME inside DIR_PATH
    """

    abs_dir_path = os.path.abspath(dir_path)
    exclude_list = exclude.split(",") if exclude else []
    exclude_dir_list = exclude_dir.split(",") if exclude_dir else []

    if not output:
        output = dir_path
    logger = LoggerFactory.get_logger(logger_types.RECURSIVE_ORGANIZE, output, save)

    if backup:
        shutil.make_archive(
            base_name=os.path.join(abs_dir_path, app.utils.config.constants.BACKUP_FILE_NAME),
            format=archive_format,
            root_dir=os.path.dirname(abs_dir_path),
            base_dir=os.path.basename(abs_dir_path),
            verbose=True,
        )

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
    logger: logging.Logger,
) -> None:
    abs_dir_path = os.path.join(parent_dir, subdir_path)
    dir_list = os.listdir(abs_dir_path)

    logger.info(log_messages.INSIDE_DIR.format(abs_dir_path=abs_dir_path))
    nested_dirs = []
    for entry in dir_list:
        abs_entry_path = os.path.join(abs_dir_path, entry)
        if os.path.isfile(abs_entry_path):
            if (
                entry == log_output.RECURSIVE_ORGANIZE_BASE
                or entry in app.utils.config.constants.SKIPPED_BACKUP_FILES
            ):
                continue

            file_extension = os.path.splitext(entry)[1]
            if not hidden and entry.startswith(".") or file_extension in exclude_list:
                logger.info(log_messages.SKIP_FILE.format(entry=entry))
                continue

            if entry.startswith("."):
                target_dir_name = TARGET_MAP["hidden"]
            else:
                target_dir_name = TARGET_MAP.get(file_extension, TARGET_MAP["default"])

            target_dir = os.path.join(abs_dir_path, target_dir_name)
            if not os.path.exists(target_dir):
                logger.info(log_messages.CREATE_FOLDER.format(target_dir=target_dir))
                os.makedirs(target_dir)

            logger.info(log_messages.MOVE_FILE.format(entry=entry, target_dir=target_dir))
            shutil.move(abs_entry_path, os.path.join(target_dir, entry))
        elif os.path.isdir(abs_entry_path):
            if entry.startswith(".") or entry in exclude_dir_list:
                logger.info(log_messages.SKIP_DIR.format(entry=entry))
                continue
            nested_dirs.append(abs_entry_path)

    for nested_dir in nested_dirs:
        _handle_files(abs_dir_path, nested_dir, exclude_list, exclude_dir_list, hidden, logger)


def _handle_files_by_flattening_subdirs(
    parent_dir: str,
    subdir_path: str,
    root_dir: str,
    exclude_list: List[str],
    exclude_dir_list: List[str],
    hidden: bool,
    logger: logging.Logger,
) -> None:
    abs_dir_path = os.path.join(parent_dir, subdir_path)
    dir_list = os.listdir(abs_dir_path)

    logger.info(log_messages.INSIDE_DIR.format(abs_dir_path=abs_dir_path))
    nested_dirs = []
    for entry in dir_list:
        abs_entry_path = os.path.join(abs_dir_path, entry)
        if os.path.isfile(abs_entry_path):
            if (
                entry == log_output.RECURSIVE_ORGANIZE_BASE
                or entry in app.utils.config.constants.SKIPPED_BACKUP_FILES
            ):
                continue

            file_extension = os.path.splitext(entry)[1]
            if not hidden and entry.startswith(".") or file_extension in exclude_list:
                logger.info(log_messages.MOVE_FILE_TO_ROOT_DIR.format(entry=entry))
                shutil.move(abs_entry_path, os.path.join(root_dir, entry))
                continue

            if entry.startswith("."):
                target_dir_name = TARGET_MAP["hidden"]
            else:
                target_dir_name = TARGET_MAP.get(file_extension, TARGET_MAP["default"])

            target_dir = os.path.join(root_dir, target_dir_name)
            if not os.path.exists(target_dir):
                logger.info(log_messages.CREATE_FOLDER.format(target_dir=target_dir))
                os.makedirs(target_dir)

            logger.info(log_messages.MOVE_FILE.format(entry=entry, target_dir=target_dir))
            shutil.move(abs_entry_path, os.path.join(target_dir, entry))
        elif os.path.isdir(abs_entry_path):
            if entry.startswith(".") or entry in exclude_dir_list:
                logger.info(log_messages.SKIP_DIR_AND_MOVE.format(entry=entry))
                shutil.move(abs_entry_path, os.path.join(root_dir, entry))
                continue
            nested_dirs.append(abs_entry_path)

    for nested_dir in nested_dirs:
        _handle_files_by_flattening_subdirs(
            abs_dir_path, nested_dir, root_dir, exclude_list, exclude_dir_list, hidden, logger
        )

    is_not_root_dir = abs_dir_path != root_dir
    is_not_one_level_nested_dir = not os.path.join(os.path.dirname(abs_dir_path), "") == root_dir
    is_not_target_dir = not os.path.basename(subdir_path) in TARGET_MAP.values()

    if is_not_root_dir and (is_not_one_level_nested_dir or is_not_target_dir):
        logger.info(log_messages.REMOVE_DIR.format(abs_dir_path=abs_dir_path))
        os.rmdir(abs_dir_path)
