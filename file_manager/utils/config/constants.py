from file_manager.logs.config import log_messages

TARGET_MAP = {
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
    ####
    "default": "other",
    "hidden": ".hidden",
}

BACKUP_FILE_NAME = "backup"
SKIPPED_BACKUP_FILES = ["backup.tar", "backup.zip"]

###################################################
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
