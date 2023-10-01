import os
import logging


def configure_logger(logger_name, output_file_name):
    logger = logging.getLogger(logger_name)
    s_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(filename=output_file_name, mode='w')

    formatter = logging.Formatter('%(message)s')
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
        files_list = [entry for entry in self.dir_list if os.path.isfile(os.path.join(self.dir_path, entry))]
        if not files_list:
            return (f"The given directory {self.dir_path} contains no files:\n\n" +
                    "\n=========================================\n")
        else:
            return (f"The given directory {self.dir_path} contains the following files:\n\n" +
                    "\n".join(files_list) +
                    "\n\n=========================================\n")

    def scan_subdirs(self):
        subdirs_list = [entry for entry in self.dir_list if os.path.isdir(os.path.join(self.dir_path, entry))]
        if not subdirs_list:
            return (f"The given directory {self.dir_path} contains no nested subdirectories:\n\n" +
                    "\n=========================================\n")
        else:
            return (f"The given directory {self.dir_path} contains the following subdirectories:\n\n" +
                    "\n".join(subdirs_list) +
                    "\n\n=========================================\n")

    def build_catalog_recursively(self, subdir_path=None):
        if subdir_path is None:
            subdir_path = self.dir_path
            subdir_list = self.dir_list
        else:
            subdir_list = os.listdir(subdir_path)

        files_list = []
        nested_dirs = []
        inner_msg = ''
        for entry in subdir_list:
            entry_path = os.path.join(subdir_path, entry)
            if os.path.isfile(entry_path):
                files_list.append(entry)
            else:
                nested_dirs.append(entry)
                inner_msg += self.build_catalog_recursively(entry_path)

        if not files_list:
            files_msg = (f"The given directory {subdir_path} contains no files:\n" +
                         "\n=========================================\n")
        else:
            files_msg = (f"The given directory {subdir_path} contains the following files:\n\n" +
                         "\n".join(files_list) +
                         "\n\n=========================================\n")

        if not nested_dirs:
            nested_dirs_msg = (f"The given directory {subdir_path} contains no nested subdirectories:\n" +
                               "\n=========================================\n")
        else:
            nested_dirs_msg = (f"The given directory {subdir_path} contains the following nested subdirectories:\n\n" +
                               "\n".join(nested_dirs) +
                               "\n\n=========================================\n")

        return files_msg + nested_dirs_msg + inner_msg

    def build_catalog(self):
        files_list = []
        nested_dirs = []
        for entry in self.dir_list:
            if os.path.isfile(os.path.join(self.dir_path, entry)):
                files_list.append(entry)
            else:
                nested_dirs.append(entry)

        if not files_list:
            files_msg = (f"The given directory {self.dir_path} contains no files:\n" +
                         "\n=========================================\n")
        else:
            files_msg = (f"The given directory {self.dir_path} contains the following files:\n\n" +
                         "\n".join(files_list) +
                         "\n\n=========================================\n")

        if not nested_dirs:
            nested_dirs_msg = (f"The given directory {self.dir_path} contains no nested subdirectories:\n" +
                               "\n=========================================\n")
        else:
            nested_dirs_msg = (
                    f"The given directory {self.dir_path} contains the following nested subdirectories:\n\n" +
                    "\n".join(nested_dirs) +
                    "\n\n=========================================\n")

        return files_msg + nested_dirs_msg


if __name__ == '__main__':
    logger = configure_logger('basic_logger', 'output.log')
    target_dir = input()

    scanner = DirScanner(target_dir)
    scanner.scan_dir()
    subdirs_list = scanner.scan_subdirs()
    files_list = scanner.scan_files()
    logger.info(files_list)

    catalog_logger = configure_logger('catalog_logger', 'catalog.log')
    catalog = scanner.build_catalog()
    catalog_logger.info(catalog)

    recursive_catalog_logger = configure_logger('recursive_catalog_logger', 'recursive_catalog.log')
    recursive_catalog = scanner.build_catalog_recursively()
    recursive_catalog_logger.info(recursive_catalog)
