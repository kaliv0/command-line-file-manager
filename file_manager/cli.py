import click

from file_manager.logs.config import log_messages
from file_manager.utils import organizer, scanner


@click.group()
def fm() -> None:
    """Good old command-line file manager\f"""
    pass


# ### scan ###
@fm.command(options_metavar="<options>")
@click.argument("dir_path", type=click.STRING, metavar="<dir_path>")
@click.option(
    "--sort",
    type=click.Choice(["name", "size", "date", "modified", "type"], case_sensitive=False),
    default="name",
    show_default=True,
    help="Sorting criteria",
)
@click.option(
    "--desc",
    is_flag=True,
    help="Display result in descending order",
)
@click.option(
    "-d",
    "--dirs",
    "list_dirs",
    is_flag=True,
    help="List subdirectories",
)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def show(dir_path: str, sort: str, desc: bool, list_dirs: bool, save: bool, output: str) -> None:
    """Short list of files or directories in <dir_path>\f"""
    scanner.show(dir_path, sort, desc, list_dirs, save, output)


#############################################################
@fm.command(options_metavar="<options>")
@click.argument("dir_path", type=click.STRING, metavar="<dir_path>")
@click.option(
    "-r",
    "--recursively",
    is_flag=True,
    help="Build catalog recursively",
)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def scan(dir_path: str, recursively: bool, save: bool, output: str) -> None:
    """Create full catalog of all files and subdirs in <dir_path>\f"""
    if recursively:
        scanner.scan_recursively(dir_path, save, output)
    else:
        scanner.scan(dir_path, save, output)


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
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def tree(dir_path: str, max_depth: int, show_hidden: bool, dirs_only: bool, save: bool, output: str) -> None:
    """Build tree of contents in <dir_path>\f"""
    scanner.build_tree(dir_path, max_depth, show_hidden, dirs_only, save, output)


#############################################################
@fm.command(options_metavar="<options>")
@click.argument("dir_path", type=click.STRING, metavar="<dir_path>")
@click.argument("name", type=click.STRING, metavar="<name>")
@click.option(
    "-r",
    "--recursively",
    is_flag=True,
    help="Search recursively",
)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def search(dir_path: str, name: str, recursively: bool, save: bool, output: str) -> None:
    """Search by <name> inside <dir_path>\f"""
    if recursively:
        scanner.search_recursively(dir_path, name, save, output)
    else:
        scanner.search(dir_path, name, save, output)


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
@click.option(
    "-r",
    "--recursively",
    is_flag=True,
    help="Compare directories recursively",
)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def diff(
    dir_path: str,
    other_path: str,
    include_hidden: bool,
    short: bool,
    one_line: bool,
    recursively: bool,
    save: bool,
    output: str,
) -> None:
    """Compare contents of <source_path> to <target_path>\f"""
    if short and one_line:
        raise click.BadParameter(log_messages.BAD_OPTS.format(flags=" | ".join(("short", "oneline"))))
    scanner.compare_directories(
        dir_path, other_path, include_hidden, short, one_line, recursively, save, output
    )


#############################################################
# ### organize ###
@fm.command(options_metavar="<options>")
@click.argument("dir_path", type=click.STRING, metavar="<dir_path>")
@click.option(
    "-x",
    "--exclude",
    type=click.STRING,
    default=None,
    show_default=True,
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
    "-b",
    "--backup",
    is_flag=True,
    help="Create an archived file of the given directory before re-organizing it",
)
@click.option(
    "-f",
    "--archive-format",
    type=click.Choice(["tar", "zip"], case_sensitive=False),
    default=None,
    show_default=True,
    help="Archive format for backup file",
)
@click.option(
    "-r",
    "--recursively",
    is_flag=True,
    help="Organize files recursively",
)
@click.option(
    "--exclude-dir",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Single or multiple directory names to be skipped separated by comma. (Used with --recursively flag)"
    "E.g. --exclude-dir audio,video",
)
@click.option(
    "--flat",
    is_flag=True,
    help="Move all files to target directories inside parent dir. (Used with --recursively flag)",
)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def tidy(
    dir_path: str,
    exclude: str,
    show_hidden: bool,
    backup: bool,
    archive_format: str,
    recursively: bool,
    exclude_dir: str,
    flat: bool,
    save: bool,
    output: str,
) -> None:
    """Organize files by extension/type inside <dir_path>\f"""
    if recursively:
        organizer.organize_files_recursively(
            dir_path, exclude, exclude_dir, flat, show_hidden, backup, archive_format, save, output
        )
    else:
        organizer.organize_files(dir_path, exclude, show_hidden, backup, archive_format, save, output)


#####################################
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
    "-b",
    "--backup",
    is_flag=True,
    help="Create an archived file of the given directory before re-organizing it",
)
@click.option(
    "-f",
    "--archive-format",
    type=click.Choice(["tar", "zip"], case_sensitive=False),
    default=None,
    show_default=True,
    help="Archive format for backup file",
)
@click.option(
    "-r",
    "--recursively",
    is_flag=True,
    help="Handle duplicates recursively",
)
@click.option(
    "-s",
    "--save",
    is_flag=True,
    help="Save log message to file",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    show_default=True,
    help="Path to output directory for the saved log file",
)
def dedup(
    dir_path: str,
    interactive: bool,
    show_hidden: bool,
    backup: bool,
    archive_format: str,
    recursively: bool,
    save: bool,
    output: str,
) -> None:
    """Find and clean-up duplicate files inside a <dir_path>\f"""
    if recursively:
        organizer.handle_duplicate_files_recursively(
            dir_path,
            interactive,
            show_hidden,
            save,
            output,
            backup,
            archive_format,
        )
    else:
        organizer.handle_duplicate_files(
            dir_path, interactive, show_hidden, backup, archive_format, save, output
        )


if __name__ == "__main__":
    fm()
