import logging
import os
import shutil
from typing import List

import click

from app.logs.config import log_messages, logger_types, log_output
from app.logs.logger_factory import LoggerFactory
from app.utils.config.file_extensions import TARGET_MAP


@click.command()
@click.argument("dir_path", type=click.STRING)
@click.option(
    "--exclude",
    type=click.STRING,
    default=None,
    help="Single or multiple file extensions to be skipped separated by comma. "
    "E.g. --exclude=.pdf,.mp3",
)
@click.option(
    "--save",
    type=click.BOOL,
    default=False,
    help="Boolean flag to save log message to file. Defaults to 'false'",
)
@click.option(
    "--output",
    type=click.STRING,
    default=None,
    help="Path to output directory for the saved log file",
)
def organize_files(dir_path: str, exclude: str, save: bool, output: str) -> None:
    """
    Search recursively by NAME keyword inside given DIR_PATH
    """

    exclude_list = exclude.split(",") if exclude else []

    dir_list = os.listdir(dir_path)
    abs_dir_path = os.path.abspath(dir_path)

    if not output:
        output = dir_path
    logger = LoggerFactory.get_logger(logger_types.ORGANIZE, output, save)

    for entry in dir_list:
        abs_entry_path = os.path.join(abs_dir_path, entry)
        if os.path.isfile(abs_entry_path):
            file_extension = os.path.splitext(entry)[1]
            if file_extension in exclude_list:
                logger.info(log_messages.SKIP_FILE.format(entry=entry))
                continue

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
    "--exclude",
    type=click.STRING,
    default=None,
    help="Single or multiple file extensions to be skipped separated by comma. "
    "E.g. --exclude=.pdf,.mp3",
)
@click.option(
    "--flat",
    type=click.BOOL,
    default=False,
    help="Boolean flag to move all files to target directories inside parent folder. Defaults to 'false'",
)
@click.option(
    "--save",
    type=click.BOOL,
    default=False,
    help="Boolean flag to save log message to file. Defaults to 'false'",
)
@click.option(
    "--output",
    type=click.STRING,
    default=None,
    help="Path to output directory for the saved log file",
)
def organize_files_recursively(
    dir_path: str, exclude: str, flat: bool, save: bool, output: str
) -> None:
    """
    Search recursively by NAME keyword inside given DIR_PATH
    """

    abs_dir_path = os.path.abspath(dir_path)
    exclude_list = exclude.split(",") if exclude else []

    if not output:
        output = dir_path
    logger = LoggerFactory.get_logger(logger_types.RECURSIVE_ORGANIZE, output, save)

    if flat:
        root_dir = os.path.join(abs_dir_path, "")
        handle_files_by_flattening_subdirs(abs_dir_path, "", root_dir, exclude_list, logger)
    else:
        _handle_files(abs_dir_path, "", exclude_list, logger)


def _handle_files(
    parent_dir: str, subdir_path: str, exclude_list: List[str], logger: logging.Logger
) -> None:
    abs_dir_path = os.path.join(parent_dir, subdir_path)
    dir_list = os.listdir(abs_dir_path)

    logger.info(log_messages.INSIDE_DIR.format(abs_dir_path=abs_dir_path))
    nested_dirs = []
    for entry in dir_list:
        abs_entry_path = os.path.join(abs_dir_path, entry)
        if os.path.isfile(abs_entry_path):
            if entry == log_output.RECURSIVE_ORGANIZE_BASE:
                continue

            file_extension = os.path.splitext(entry)[1]
            if file_extension in exclude_list:
                logger.info(log_messages.SKIP_FILE.format(entry=entry))
                continue

            target_dir_name = TARGET_MAP.get(file_extension, TARGET_MAP["default"])
            target_dir = os.path.join(abs_dir_path, target_dir_name)

            if not os.path.exists(target_dir):
                logger.info(log_messages.CREATE_FOLDER.format(target_dir=target_dir))
                os.makedirs(target_dir)

            logger.info(log_messages.MOVE_FILE.format(entry=entry, target_dir=target_dir))
            shutil.move(abs_entry_path, os.path.join(target_dir, entry))
        elif os.path.isdir(abs_entry_path):
            nested_dirs.append(abs_entry_path)

    for nested_dir in nested_dirs:
        _handle_files(abs_dir_path, nested_dir, exclude_list, logger)


def handle_files_by_flattening_subdirs(
    parent_dir: str,
    subdir_path: str,
    root_dir: str,
    exclude_list: List[str],
    logger: logging.Logger,
) -> None:
    abs_dir_path = os.path.join(parent_dir, subdir_path)
    dir_list = os.listdir(abs_dir_path)

    logger.info(log_messages.INSIDE_DIR.format(abs_dir_path=abs_dir_path))
    nested_dirs = []
    for entry in dir_list:
        abs_entry_path = os.path.join(abs_dir_path, entry)
        if os.path.isfile(abs_entry_path):
            if entry == log_output.RECURSIVE_ORGANIZE_BASE:
                continue

            file_extension = os.path.splitext(entry)[1]
            if file_extension in exclude_list:
                logger.info(log_messages.SKIP_FILE.format(entry=entry))
                continue

            target_dir_name = TARGET_MAP.get(file_extension, TARGET_MAP["default"])
            target_dir = os.path.join(root_dir, target_dir_name)

            if not os.path.exists(target_dir):
                logger.info(log_messages.CREATE_FOLDER.format(target_dir=target_dir))
                os.makedirs(target_dir)

            logger.info(log_messages.MOVE_FILE.format(entry=entry, target_dir=target_dir))
            shutil.move(abs_entry_path, os.path.join(target_dir, entry))
        elif os.path.isdir(abs_entry_path):
            nested_dirs.append(abs_entry_path)

    for nested_dir in nested_dirs:
        handle_files_by_flattening_subdirs(abs_dir_path, nested_dir, root_dir, exclude_list, logger)

    if abs_dir_path != root_dir:
        logger.info(log_messages.REMOVE_DIR.format(abs_dir_path=abs_dir_path))
        os.rmdir(abs_dir_path)
