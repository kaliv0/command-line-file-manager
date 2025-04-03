LOG_FORMAT = "%(message)s"

DELIMITER = "=========================================\n"
NO_FILES = "'{dir_path}' contains no files\n" + DELIMITER
LISTED_FILES = "'{dir_path}' contains the following files:\n\t- {entries_list}\n" + DELIMITER

DUPLICATE_DELIMITER = "-----------------------------------------\n"
NO_DUPLICATE_FILES = "'{dir_path}' contains no duplicate files\n"
LISTED_DUPLICATE_FILES = "'{dir_path}' contains the following duplicate files:\n{display_list}"

NO_SUBDIRS = "'{dir_path}' contains no nested subdirectories\n" + DELIMITER
NESTED_SUBDIRS = "'{dir_path}' contains the following subdirectories:\n\t- {entries_list}\n" + DELIMITER

NOT_FOUND = "Nothing found\n"
FOUND_BY_NAME = "Inside directory '{dir_path}' the given (partial) keyword '{sequence}' was found\n"
FOUND_BY_PATTERN = "Inside directory '{dir_path}' the given pattern '{sequence}' was found\n"
FOUND_FILES_BY_NAME = "- in the following file names:\n\t- {files_list}\n"
FOUND_DIRS_BY_NAME = "- in the following subdirectory names:\n\t- {subdir_list}\n"

CREATE_DIR = "Creating directory {target_dir}\n"
MOVE_FILE = "Moving {entry} to {target_dir}\n"

INSIDE_DIR = "----- Inside {abs_dir_path} -----\n"

SKIP_FILE = "Skipping {entry}\n"
SKIP_DIR = "Skipping {entry} directory\n"
MOVE_FILE_TO_ROOT_DIR = "Moving {entry} to root directory\n"
SKIP_DIR_AND_MOVE = "Moving {entry} directory without stepping inside\n"

REMOVE_DIR = "Removing {abs_dir_path}\n"
MERGE_FILES = "Merging duplicates: {entry} into '{target_name}'\n"
PRE_MERGE_PROMPT = "Please enter file name for the following duplicates: {entry}\n"

DIRS_DIFF = DELIMITER + "Diff '{left}' -- '{right}':\n"
DELIM_LIST = "{delimiter}{list}\n"
DIFF_STATS = "- Only in '{dir}'" + DELIM_LIST
SAME_FILES = f"- Identical files{DELIM_LIST}"
DIFF_FILES = f"- Differing files{DELIM_LIST}"
TROUBLE_FILES = f"- Trouble with common files{DELIM_LIST}"
COMMON_SUBDIRS = f"- Common subdirectories{DELIM_LIST}"
COMMON_TROUBLE = f"- Common problematic cases{DELIM_LIST}"

BAD_OPTS = "Mutually exclusive flags: {flags}\n"
IDENTICAL_PATHS = "Paths are identical\n"
