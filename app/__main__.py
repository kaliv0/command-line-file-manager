import click

from app.util import dir_scanner


@click.group()
def cli():
    pass


cli.add_command(dir_scanner.scan_files)
cli.add_command(dir_scanner.scan_subdirs)
cli.add_command(dir_scanner.build_catalog)
cli.add_command(dir_scanner.build_catalog_recursively)
cli.add_command(dir_scanner.build_tree)
cli.add_command(dir_scanner.build_pretty_tree)
cli.add_command(dir_scanner.search_by_name)

# name = input()
# entries_by_name = scanner.search_by_name(name)
# entries_by_name = scanner.search_by_name_recursively(name)
# logger.info(entries_by_name)
