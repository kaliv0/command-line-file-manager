import click

from app.util import dir_scanner


@click.group()
def cli():
    pass


cli.add_command(dir_scanner.scan_files)  # noqa
cli.add_command(dir_scanner.scan_subdirs)  # noqa
cli.add_command(dir_scanner.build_catalog)  # noqa
cli.add_command(dir_scanner.build_catalog_recursively)  # noqa

# tree_logger = LoggerFactory.get_logger(logger_types.TREE, output_dir)
# tree_catalog = scanner.build_tree()
# # tree_catalog = scanner.build_pretty_tree()
# tree_logger.info(tree_catalog)

# name = input()
# entries_by_name = scanner.search_by_name(name)
# entries_by_name = scanner.search_by_name_recursively(name)
# logger.info(entries_by_name)
