import os

from log import log_messages


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
        subdir_list = [
            entry
            for entry in self.dir_list
            if os.path.isdir(os.path.join(self.dir_path, entry))
        ]
        if not subdir_list:
            return log_messages.NO_SUBDIRS.format(dir_path=self.dir_path)
        else:
            return log_messages.NESTED_SUBDIRS.format(
                dir_path=self.dir_path, subdir_list="\n".join(subdir_list)
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
                dir_path=self.dir_path, subdir_list="\n".join(nested_dirs)
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
            files_msg = log_messages.NO_FILES.format(dir_path=subdir_path)
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
                dir_path=subdir_path, subdir_list="\n".join(nested_dirs)
            )

        return files_msg + nested_dirs_msg + inner_msg
