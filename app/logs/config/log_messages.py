LOG_FORMAT = "%(message)s"

DELIMITER = "\n=========================================\n"

NO_FILES = "The given directory '{dir_path}' contains no files:\n\n" + DELIMITER

LISTED_FILES = (
    "The given directory '{dir_path}' contains the following files:\n"
    + "\n{files_list}\n"
    + DELIMITER
)

NO_SUBDIRS = "The given directory '{dir_path}' contains no nested subdirectories:\n\n" + DELIMITER

NESTED_SUBDIRS = (
    "The given directory '{dir_path}' contains the following subdirectories:\n"
    + "\n{subdir_list}\n"
    + DELIMITER
)

NOT_FOUND = "Nothing found.\n"
FOUND_BY_NAME = "Inside directory '{dir_path}' the given keyword '{keyword}' was found\n"
FOUND_FILES_BY_NAME = "- in the following file names:\n" + "\t- {files_list}\n"
FOUND_DIRS_BY_NAME = "- in the following subdirectory names:\n" + "\t- {subdir_list}\n"

CREATE_FOLDER = "Creating folder {target_dir}"
MOVE_FILE = "Moving {entry} to {target_dir}"

INSIDE_DIR = "----- Inside {abs_dir_path} -----"

SKIP_FILE = "Skipping {entry}"
SKIP_DIR = "Skipping {entry} directory"
MOVE_FILE_TO_ROOT_DIR = "Moving {entry} to root directory"
SKIP_DIR_AND_MOVE = "Moving {entry} directory without stepping inside"

REMOVE_DIR = "Removing {abs_dir_path}"
