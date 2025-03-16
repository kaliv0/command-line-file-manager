LOG_FORMAT = "%(message)s"

DELIMITER = "=========================================\n"
NO_FILES = "'{dir_path}' contains no files\n" + DELIMITER
LISTED_FILES = "'{dir_path}' contains the following files:\n\t- {entries_list}\n" + DELIMITER

DUPLICATE_DELIMITER = "-----------------------------------------\n"
NO_DUPLICATE_FILES = "'{dir_path}' contains no duplicate files"
LISTED_DUPLICATE_FILES = "'{dir_path}' contains the following duplicate files:\n{display_list}"

NO_SUBDIRS = "'{dir_path}' contains no nested subdirectories\n" + DELIMITER
NESTED_SUBDIRS = "'{dir_path}' contains the following subdirectories:\n\t- {entries_list}\n" + DELIMITER

NOT_FOUND = "Nothing found"
FOUND_BY_NAME = "Inside directory '{dir_path}' the given keyword '{keyword}' was found{delimiter}"
FOUND_FILES_BY_NAME = "- in the following file names:\n\t- {files_list}{delimiter}"
FOUND_DIRS_BY_NAME = "- in the following subdirectory names:\n\t- {subdir_list}{delimiter}"

CREATE_DIR = "Creating directory {target_dir}"
MOVE_FILE = "Moving {entry} to {target_dir}"

INSIDE_DIR = "----- Inside {abs_dir_path} -----"

SKIP_FILE = "Skipping {entry}"
SKIP_DIR = "Skipping {entry} directory"
MOVE_FILE_TO_ROOT_DIR = "Moving {entry} to root directory"
SKIP_DIR_AND_MOVE = "Moving {entry} directory without stepping inside"

REMOVE_DIR = "Removing {abs_dir_path}"
MERGE_FILES = "Merging duplicates: {entry} into {target_name}"
PRE_MERGE_PROMPT = "Please enter file name for the following duplicates: {entry}\n"

DIRS_DIFF = DELIMITER + "Diff '{left}' -- '{right}':"
DELIM_LIST = "{delimiter}{list}"
DIFF_STATS = "- Only in '{dir}'" + DELIM_LIST
SAME_FILES = "- Identical files" + DELIM_LIST
DIFF_FILES = "- Differing files" + DELIM_LIST
TROUBLE_FILES = "- Trouble with common files" + DELIM_LIST
COMMON_SUBDIRS = "- Common subdirectories" + DELIM_LIST
COMMON_TROUBLE = "- Common problematic cases" + DELIM_LIST

BAD_OPTS = "Mutually exclusive flags: {flags}"
IDENTICAL_PATHS = "Paths are identical"
