import click

from file_manager.logs import log_messages
from file_manager.utils import organizer, scanner
from file_manager.utils.decorator import save_logs, sort_order_results, create_backup, recursive


@click.group()
def fm() -> None:
    """Good old command-line file manager\f"""
    pass


# ### scan ###
@fm.command(options_metavar="<options>")
@click.argument("dir_path", type=click.STRING, metavar="<dir_path>")
@click.option(
    "-d",
    "--dirs",
    "list_dirs",
    is_flag=True,
    help="List subdirectories",
)
@sort_order_results
@save_logs
def show(dir_path: str, sort: str, desc: bool, list_dirs: bool, save: bool, output: str, log: str) -> None:
    """Short list of files or directories in <dir_path>\f"""
    scanner.show(dir_path, sort, desc, list_dirs, save, output, log)


#############################################################
@fm.command(options_metavar="<options>")
@click.argument("dir_path", type=click.STRING, metavar="<dir_path>")
@recursive
@sort_order_results
@save_logs
def scan(dir_path: str, recursively: bool, sort: str, desc: bool, save: bool, output: str, log: str) -> None:
    """Create full catalog of all files and subdirs in <dir_path>\f"""
    if recursively:
        scanner.scan_recursively(dir_path, sort, desc, save, output, log)
    else:
        scanner.scan(dir_path, sort, desc, save, output, log)


#############################################################
@fm.command(options_metavar="<options>")
@click.argument("dir_path", type=click.STRING, metavar="<dir_path>")
@click.option(
    "-l",
    "--level",
    "max_depth",
    type=click.IntRange(0),
    help="Include hidden files and subdirectories",
)
@click.option(
    "-h",
    "--hidden",
    "show_hidden",
    is_flag=True,
    help="Include hidden files and subdirectories",
)
@click.option(
    "-d",
    "--dirs",
    "dirs_only",
    is_flag=True,
    help="Show only nested directories",
)
@save_logs
def tree(
    dir_path: str, max_depth: int, show_hidden: bool, dirs_only: bool, save: bool, output: str, log: str
) -> None:
    """Build tree of contents in <dir_path>\f"""
    scanner.build_tree(dir_path, max_depth, show_hidden, dirs_only, save, output, log)


#############################################################
@fm.command(options_metavar="<options>")
@click.argument("dir_path", type=click.STRING, metavar="<dir_path>")
@click.argument("name", type=click.STRING, metavar="<name>")
@click.option(
    "-x",
    "--regex",
    "use_regex",
    is_flag=True,
    help="Search by regex pattern",
)
@recursive
@save_logs
def search(
    dir_path: str, name: str, use_regex: bool, recursively: bool, save: bool, output: str, log: str
) -> None:
    """Search by <name> inside <dir_path>\f"""
    if recursively:
        scanner.search_recursively(dir_path, name, use_regex, save, output, log)
    else:
        scanner.search(dir_path, name, use_regex, save, output, log)


#############################################################
@fm.command(options_metavar="<options>")
@click.argument("dir_path", type=click.STRING, metavar="<source_path>")
@click.argument("other_path", type=click.STRING, metavar="<target_path>")
@click.option(
    "-h",
    "--hidden",
    "include_hidden",
    is_flag=True,
    help="Include hidden files and subdirectories",
)
@click.option(
    "--short",
    is_flag=True,
    help="Show short statistics (count only)",
)
@click.option(
    "--oneline",
    "one_line",
    is_flag=True,
    help="Show compact list on single line",
)
@recursive
@save_logs
def diff(
    dir_path: str,
    other_path: str,
    include_hidden: bool,
    short: bool,
    one_line: bool,
    recursively: bool,
    save: bool,
    output: str,
    log: str,
) -> None:
    """Compare contents of <source_path> to <target_path>\f"""
    if short and one_line:
        raise click.BadParameter(log_messages.BAD_OPTS.format(flags=" | ".join(("short", "oneline"))))
    scanner.compare_directories(
        dir_path, other_path, include_hidden, short, one_line, recursively, save, output, log
    )


#############################################################
# ### organize ###
@fm.command(options_metavar="<options>")
@click.argument("dir_path", type=click.STRING, metavar="<dir_path>")
@click.option(
    "-i",
    "--interactive",
    is_flag=True,
    help="Prompt for destination file name before merging duplicates",
)
@click.option(
    "-h",
    "--hidden",
    "show_hidden",
    is_flag=True,
    help="Include hidden files",
)
@click.option(
    "-r",
    "--recursively",
    is_flag=True,
    help="Handle duplicates recursively",
)
@create_backup
@save_logs
def dedup(
    dir_path: str,
    interactive: bool,
    show_hidden: bool,
    backup: bool,
    archive_format: str,
    recursively: bool,
    save: bool,
    output: str,
    log: str,
) -> None:
    """Find and clean-up duplicate files inside a <dir_path>\f"""
    if recursively:
        organizer.handle_duplicate_files_recursively(
            dir_path,
            interactive,
            show_hidden,
            save,
            output,
            log,
            backup,
            archive_format,
        )
    else:
        organizer.handle_duplicate_files(
            dir_path, interactive, show_hidden, save, output, log, backup, archive_format
        )


#####################################
@fm.command(options_metavar="<options>")
@click.argument("dir_path", type=click.STRING, metavar="<dir_path>")
@click.option(
    "-x",
    "--exclude",
    type=click.STRING,
    default=None,
    help="Single or multiple file extensions to be skipped separated by comma e.g. --exclude .pdf,.mp3",
)
@click.option(
    "-h",
    "--hidden",
    "show_hidden",
    is_flag=True,
    help="Include hidden files",
)
@click.option(
    "--exclude-dir",
    type=click.STRING,
    default=None,
    help="Single or multiple directory names to be skipped separated by comma. (Used with --recursively flag) E.g. --exclude-dir audio,video",
)
@click.option(
    "--flat",
    is_flag=True,
    help="Move all files to target directories inside parent dir. (Used with --recursively flag)",
)
@recursive
@create_backup
@save_logs
def tidy(
    dir_path: str,
    exclude: str,
    show_hidden: bool,
    exclude_dir: str,
    flat: bool,
    recursively: bool,
    backup: bool,
    archive_format: str,
    save: bool,
    output: str,
    log: str,
) -> None:
    """Organize files by extension/type inside <dir_path>\f"""
    if recursively:
        organizer.organize_files_recursively(
            dir_path, exclude, exclude_dir, flat, show_hidden, backup, archive_format, save, output, log
        )
    else:
        organizer.organize_files(dir_path, exclude, show_hidden, backup, archive_format, save, output, log)


if __name__ == "__main__":
    fm()
