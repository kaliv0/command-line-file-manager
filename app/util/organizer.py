import os
import shutil

import click

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


@click.command()
@click.argument("dir_path", type=click.STRING)
# @click.option(
#     "--save",
#     type=click.BOOL,
#     default=False,
#     help="Boolean flag to save log message to file. Defaults to 'false'",
# )
# @click.option(
#     "--output",
#     type=click.STRING,
#     default=None,
#     help="Path to output directory for the saved log file",
# )
def organize_files(dir_path: str) -> None:
    dir_list = os.listdir(dir_path)
    for entry in dir_list:
        if os.path.isfile(os.path.join(dir_path, entry)):
            file_extension = os.path.splitext(entry)[1]
            target_dir_name = FILE_EXTENSIONS.get(file_extension, "other")
            target_dir = os.path.join(os.path.abspath(dir_path), target_dir_name)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            shutil.move(os.path.join(os.path.abspath(dir_path), entry), os.path.join(target_dir, entry))
