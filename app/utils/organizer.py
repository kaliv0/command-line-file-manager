import os
import shutil
from typing import Optional, List

import click

from app.logs import logger_types, log_messages
from app.utils.common import save_logs_to_file

FILE_EXTENSIONS = {
    # images
    ".jpg": "images",
    ".jpeg": "images",
    ".png": "images",
    ".gif": "images",
    ".svg": "images",
    ".heic": "images",
    ".tif": "images",
    ".tiff": "images",
    # videos
    ".mp4": "videos",
    ".mpeg-4": "videos",
    ".mov": "videos",
    ".avi": "videos",
    ".webm": "videos",
    # music
    ".mp3": "music",
    ".m4a": "music",
    ".wav": "music",
    ".flac": "music",
    ".ogg": "music",
    # books
    ".pdf": "books",
    ".djvu": "books",
    ".epub": "books",
    ".fb2": "books",
    # docs
    ".xlsx": "docs",
    ".csv": "docs",
    ".docx": "docs",
    ".doc": "docs",
    ".rtf": "docs",
    ".txt": "docs",
    ".pptx": "docs",
    ".ppt": "docs",
    ".key": "docs",
    # archive
    ".rar": "archive",
    ".zip": "archive",
    ".gz": "archive",
    ".tar": "archive",
    # torrent
    ".torrent": "torrent",
}

COMMON_DIR = "other"


@click.command()
@click.argument("dir_path", type=click.STRING)
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
def organize_files(dir_path: str, save: bool, output: str) -> None:
    """
    Search recursively by NAME keyword inside given DIR_PATH
    """

    dir_list = os.listdir(dir_path)
    abs_dir_path = os.path.abspath(dir_path)
    log_msg = []
    for entry in dir_list:
        abs_entry_path = os.path.join(abs_dir_path, entry)
        if os.path.isfile(abs_entry_path):
            file_extension = os.path.splitext(entry)[1]
            target_dir_name = FILE_EXTENSIONS.get(file_extension, COMMON_DIR)
            target_dir = os.path.join(abs_dir_path, target_dir_name)
            if not os.path.exists(target_dir):
                dir_msg = log_messages.CREATE_FOLDER.format(target_dir=target_dir)
                click.echo(dir_msg)
                log_msg.append(dir_msg)
                os.makedirs(target_dir)
            file_msg = log_messages.MOVE_FILE.format(entry=entry, target_dir=target_dir)
            click.echo(file_msg)
            log_msg.append(file_msg)
            shutil.copy(abs_entry_path, os.path.join(target_dir, entry))

    if save:
        final_msg = "\n".join(log_msg)
        save_logs_to_file(output, dir_path, final_msg, logger_types.ORGANIZE)


@click.command()
@click.argument("dir_path", type=click.STRING)
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
def organize_files_recursively(dir_path: str, save: bool, output: str) -> None:
    """
    Search recursively by NAME keyword inside given DIR_PATH
    """

    log_msg = []
    _handle_files(os.path.abspath(dir_path), "", save, log_msg)
    if save:
        final_msg = "\n".join(log_msg)
        save_logs_to_file(output, dir_path, final_msg, logger_types.RECURSIVE_ORGANIZE)


def _handle_files(parent_dir: str, subdir_path: Optional[str], save: bool, log_msg: List) -> None:
    abs_dir_path = os.path.join(parent_dir, subdir_path)
    dir_list = os.listdir(abs_dir_path)

    header_msg = log_messages.INSIDE_DIR.format(abs_dir_path=abs_dir_path)
    click.echo(header_msg)
    log_msg.append(header_msg)

    nested_dirs = []
    for entry in dir_list:
        abs_entry_path = os.path.join(abs_dir_path, entry)
        if os.path.isfile(abs_entry_path):
            file_extension = os.path.splitext(entry)[1]
            target_dir_name = FILE_EXTENSIONS.get(file_extension, COMMON_DIR)
            target_dir = os.path.join(abs_dir_path, target_dir_name)

            if not os.path.exists(target_dir):
                dir_msg = log_messages.CREATE_FOLDER.format(target_dir=target_dir)
                click.echo(dir_msg)
                log_msg.append(dir_msg)
                os.makedirs(target_dir)

            file_msg = log_messages.MOVE_FILE.format(entry=entry, target_dir=target_dir)
            click.echo(file_msg)
            log_msg.append(file_msg)
            shutil.copy(abs_entry_path, os.path.join(target_dir, entry))
        elif os.path.isdir(abs_entry_path):
            nested_dirs.append(abs_entry_path)

    for nested_dir in nested_dirs:
        _handle_files(abs_dir_path, nested_dir, save, log_msg)
