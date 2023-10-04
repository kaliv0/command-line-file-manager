import os

import emoji
from directory_tree import display_tree

from src.log import log_messages


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

    def build_tree(self):
        folder_emoji = emoji.emojize(":file_folder:")
        file_emoji = emoji.emojize(":page_with_curl:")

        tree_msg = ""
        for root, _, files in os.walk(self.dir_path):
            level = root.count(os.sep) - 1
            indent = " " * 4 * level
            tree_msg += "{}{} {}/\n".format(
                indent, folder_emoji, os.path.abspath(root)
            )
            sub_indent = " " * 4 * (level + 1)
            for file in files:
                tree_msg += "{}{} {}\n".format(sub_indent, file_emoji, file)
        return tree_msg

    def build_pretty_tree(self, show_hidden=True):
        return display_tree(
            self.dir_path, string_rep=True, show_hidden=show_hidden
        )

    def search_by_name(self, name):
        files_list = []
        nested_dirs = []
        for entry in self.dir_list:
            if name in entry:
                if os.path.isfile(os.path.join(self.dir_path, entry)):
                    files_list.append(entry)
                else:
                    nested_dirs.append(entry)
        return log_messages.FOUND_BY_NAME.format(
            files_list="\n\t".join(files_list),
            nested_dirs="\n\t".join(nested_dirs),
        )

    def search_by_name_recursively(self, name, subdir_path=None):
        if subdir_path is None:
            subdir_path = self.dir_path
            subdir_list = self.dir_list
        else:
            subdir_list = os.listdir(subdir_path)

        files_list = []
        nested_dirs = []
        valid_dirs = []
        inner_msg = ""
        for entry in subdir_list:
            entry_path = os.path.join(subdir_path, entry)
            if os.path.isfile(entry_path) and name in entry:
                files_list.append(entry)
            elif os.path.isdir(entry_path):
                if name in entry:
                    valid_dirs.append(entry)
                nested_dirs.append(entry)
                inner_msg += self.search_by_name_recursively(name, entry_path)

        if not files_list and not valid_dirs:
            return ""
        log_msg = log_messages.FOUND_BY_NAME.format(
            dir_path=subdir_path, keyword=name
        )
        if files_list:
            log_msg += log_messages.FOUND_FILES_BY_NAME.format(
                files_list="\n\t- ".join(files_list),
            )
        if valid_dirs:
            log_msg += log_messages.FOUND_DIRS_BY_NAME.format(
                subdir_list="\n\t- ".join(valid_dirs),
            )
        return log_msg + log_messages.DELIMITER + inner_msg
