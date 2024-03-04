import click

from app.cli.commands import (
    build_catalog,
    build_catalog_recursively,
    build_pretty_tree,
    build_tree,
    handle_duplicate_files,
    handle_duplicate_files_recursively,
    organize_files,
    organize_files_recursively,
    scan_files,
    scan_subdirs,
    search_by_name,
    search_by_name_recursively,
)


@click.group()
def cli() -> None:
    pass


cli.add_command(scan_files)
cli.add_command(scan_subdirs)
cli.add_command(build_catalog)
cli.add_command(build_catalog_recursively)
cli.add_command(build_tree)
cli.add_command(build_pretty_tree)
cli.add_command(search_by_name)
cli.add_command(search_by_name_recursively)

cli.add_command(organize_files)
cli.add_command(organize_files_recursively)
cli.add_command(handle_duplicate_files)
cli.add_command(handle_duplicate_files_recursively)
