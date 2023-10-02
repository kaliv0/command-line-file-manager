import os
import logging

import log_messages


def configure_logger(logger_name, output_file_name):
    logger = logging.getLogger(logger_name)
    s_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(filename=output_file_name, mode="w")

    formatter = logging.Formatter("%(message)s")
    s_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)

    logger.addHandler(s_handler)
    logger.addHandler(f_handler)

    logger.setLevel(logging.INFO)
    return logger


class DirScanner:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.dir_list = None

    def scan_dir(self):
        self.dir_list = os.listdir(self.dir_path)

    def scan_files(self):
        files_list = [
            entry
            for entry in self.dir_list
            if os.path.isfile(os.path.join(self.dir_path, entry))
        ]
        if not files_list:
            return log_messages.NO_FILES.format(dir_path=self.dir_path)
        else:
            return log_messages.LISTED_FILES.format(
                dir_path=self.dir_path, files_list="\n".join(files_list)
            )

    def scan_subdirs(self):
        subdirs_list = [
            entry
            for entry in self.dir_list
            if os.path.isdir(os.path.join(self.dir_path, entry))
        ]
        if not subdirs_list:
            return log_messages.NO_SUBDIRS.format(dir_path=self.dir_path)
        else:
            return log_messages.NESTED_SUBDIRS.format(
                dir_path=self.dir_path, subdirs_list="\n".join(subdirs_list)
            )

    def build_catalog(self):
        files_list = []
        nested_dirs = []
        for entry in self.dir_list:
            if os.path.isfile(os.path.join(self.dir_path, entry)):
                files_list.append(entry)
            else:
                nested_dirs.append(entry)

        if not files_list:
            files_msg = log_messages.NO_FILES.format(self.dir_path)
        else:
            files_msg = log_messages.LISTED_FILES.format(
                dir_path=self.dir_path, files_list="\n".join(files_list)
            )

        if not nested_dirs:
            nested_dirs_msg = log_messages.NO_SUBDIRS.format(
                dir_path=self.dir_path
            )
        else:
            nested_dirs_msg = log_messages.NESTED_SUBDIRS.format(
                dir_path=self.dir_path, subdirs_list="\n".join(nested_dirs)
            )

        return files_msg + nested_dirs_msg

    def build_catalog_recursively(self, subdir_path=None):
        if subdir_path is None:
            subdir_path = self.dir_path
            subdir_list = self.dir_list
        else:
            subdir_list = os.listdir(subdir_path)

        files_list = []
        nested_dirs = []
        inner_msg = ""
        for entry in subdir_list:
            entry_path = os.path.join(subdir_path, entry)
            if os.path.isfile(entry_path):
                files_list.append(entry)
            else:
                nested_dirs.append(entry)
                inner_msg += self.build_catalog_recursively(entry_path)

        if not files_list:
            files_msg = log_messages.NO_FILES.format(subdir_path)
        else:
            files_msg = log_messages.LISTED_FILES.format(
                dir_path=subdir_path, files_list="\n".join(files_list)
            )

        if not nested_dirs:
            nested_dirs_msg = log_messages.NO_SUBDIRS.format(
                dir_path=subdir_path
            )
        else:
            nested_dirs_msg = log_messages.NESTED_SUBDIRS.format(
                dir_path=subdir_path, subdirs_list="\n".join(nested_dirs)
            )

        return files_msg + nested_dirs_msg + inner_msg


if __name__ == "__main__":
    # TODO: extract logging setup and use logger factory
    logger = configure_logger("basic_logger", "output.log")
    target_dir = input()

    scanner = DirScanner(target_dir)
    scanner.scan_dir()
    subdirs_list = scanner.scan_subdirs()
    files_list = scanner.scan_files()
    logger.info(files_list)

    catalog_logger = configure_logger("catalog_logger", "catalog.log")
    catalog = scanner.build_catalog()
    catalog_logger.info(catalog)

    recursive_catalog_logger = configure_logger(
        "recursive_catalog_logger", "recursive_catalog.log"
    )
    recursive_catalog = scanner.build_catalog_recursively()
    recursive_catalog_logger.info(recursive_catalog)
