import click

from file_manager.cli.commands import (
    build_catalog,
    build_pretty_tree,
    build_tree,
    handle_duplicate_files,
    organize_files,
    scan_files,
    scan_subdirs,
    search_by_name,
    compare_directories,
)

# class AliasedGroup(click.Group):
#     CMD_ALIASES = {
#         "scan" : scan_files,
#         "scan-dir": scan_subdirs,
#         "catalog": build_catalog,
#         "tree": build_tree,
#         "search": search_by_name,
#         "diff": compare_directories,
#         "organize": organize_files,
#         "dedup": handle_duplicate_files
#
#     }
#
#     def get_command(self, ctx, cmd_name):
#         try:
#             cmd_name = self.CMD_ALIASES[cmd_name].name
#         except KeyError:
#             pass
#         return super().get_command(ctx, cmd_name)


@click.group()
def cli() -> None:
    pass


cli.add_command(scan_files)
cli.add_command(scan_subdirs)
cli.add_command(build_catalog)
cli.add_command(build_tree)
cli.add_command(build_pretty_tree)
cli.add_command(search_by_name)
cli.add_command(compare_directories)
cli.add_command(organize_files)
cli.add_command(handle_duplicate_files)

if __name__ == "__main__":
    cli()
