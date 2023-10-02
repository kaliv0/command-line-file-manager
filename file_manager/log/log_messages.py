DELIMITER = "\n=========================================\n"

NO_FILES = "The given directory {dir_path} contains no files:\n\n" + DELIMITER

LISTED_FILES = (
    "The given directory {dir_path} contains the following files:\n"
    + "\n{files_list}\n"
    + DELIMITER
)

NO_SUBDIRS = (
    "The given directory {dir_path} contains no nested subdirectories:\n\n"
    + DELIMITER
)

NESTED_SUBDIRS = (
    "The given directory {dir_path} contains the following subdirectories:\n"
    + "\n{subdir_list}\n"
    + DELIMITER
)
