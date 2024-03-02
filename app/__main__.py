import click

from app.cli.commands import (
    scan_files,
    scan_subdirs,
    build_catalog_recursively,
    build_tree,
    build_pretty_tree,
    search_by_name,
    search_by_name_recursively,
    build_catalog,
)
from app.utils.organizer import organize_files, organize_files_recursively, handle_duplicate_files


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
