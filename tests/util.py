from filecmp import dircmp
from os.path import getsize

changed_files = {}
deleted_files = {}
added_files = {}


def diff_file_size(file1, file2):
    return getsize(file2) - getsize(file1)


def diff_report():
    # for k, v in deleted_files.items():
    #     print(k, v)
    #
    # for k, v in added_files.items():
    #     print(k, v)
    #
    # for k, v in changed_files.items():
    #     print(k, v)
    return len(changed_files), len(deleted_files), len(added_files)


def compare_dir(path):
    for changed_file in path.diff_files:
        file1 = "{0}/{1}".format(path.left, changed_file)
        file2 = "{0}/{1}".format(path.right, changed_file)
        changed_files[file2] = diff_file_size(file1, file2)

    for deleted_file in path.left_only:
        file1 = "{0}/{1}".format(path.right, deleted_file)
        deleted_files[file1] = "DELETED!"

    for added_file in path.right_only:
        file1 = "{0}/{1}".format(path.right, added_file)
        added_files[file1] = "ADDED!"

    for sub_dir in path.subdirs.values():
        compare_dir(sub_dir)


def compare(source, target):
    cmp_obj = dircmp(source, target)
    compare_dir(cmp_obj)
    return diff_report()
