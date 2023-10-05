import click

from app.util import dir_scanner


@click.group()
def cli():
    pass


cli.add_command(dir_scanner.scan_files)  # noqa


# scanner = DirScanner(target_dir)
# # scanner.scan_dir()
# subdir_list = scanner.scan_subdirs()
# logger.info(subdir_list)
# files_list = scanner.scan_files(
#     sort_criteria=sort_criteria, reverse_order=reverse_order
# )
# logger.info(files_list)

# catalog_logger = LoggerFactory.get_logger(logger_types.CATALOG, output_dir)
# catalog = scanner.build_catalog()
# catalog_logger.info(catalog)
#
# recursive_catalog_logger = LoggerFactory.get_logger(
#     logger_types.RECURSIVE, output_dir
# )
# recursive_catalog = scanner.build_catalog_recursively()
# recursive_catalog_logger.info(recursive_catalog)
#
# tree_logger = LoggerFactory.get_logger(logger_types.TREE, output_dir)
# tree_catalog = scanner.build_tree()
# # tree_catalog = scanner.build_pretty_tree()
# tree_logger.info(tree_catalog)

# name = input()
# entries_by_name = scanner.search_by_name(name)
# entries_by_name = scanner.search_by_name_recursively(name)
# logger.info(entries_by_name)
