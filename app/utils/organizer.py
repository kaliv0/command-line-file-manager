import os
import shutil

import click

from app.logs import logger_types
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
    if save:
        # TODO: use list instead and "\n".join at the end?
        log_msg = ""
    for entry in dir_list:
        abs_entry_path = os.path.join(abs_dir_path, entry)
        if os.path.isfile(abs_entry_path):
            file_extension = os.path.splitext(entry)[1]
            target_dir_name = FILE_EXTENSIONS.get(file_extension, COMMON_DIR)
            target_dir = os.path.join(abs_dir_path, target_dir_name)
            if not os.path.exists(target_dir):
                click.echo(f"Creating folder {target_dir}")
                if save:
                    log_msg += f"Creating folder {target_dir}" + "\n"
                os.makedirs(target_dir)
            click.echo(f"Moving {entry} to {target_dir}")
            if save:
                log_msg += f"Moving {entry} to {target_dir}" + "\n"
            shutil.copy(abs_entry_path, os.path.join(target_dir, entry))

    if save:
        save_logs_to_file(output, dir_path, log_msg, logger_types.ORGANIZE)
