import click

from file_manager.utils import organizer, scanner


@click.group()
def fm() -> None:
    pass


# ### scan ###
@fm.command(short_help="DIR_PATH: Path to directory to be scanned")
@click.argument("dir_path", type=click.STRING)
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
    scanner.show(dir_path, sort, desc, list_dirs, save, output)


#############################################################
@fm.command()
@click.argument("dir_path", type=click.STRING)
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
def scan(dir_path: str, recursively: bool, save: bool, output: str):
    """DIR_PATH: Path to directory to be scanned"""
    if recursively:
        scanner.scan_recursively(dir_path, save, output)
    else:
        scanner.scan(dir_path, save, output)


#############################################################
@fm.command()
@click.argument("dir_path", type=click.STRING)
@click.option(
    "-h",
    "--hidden",
    "show_hidden",
    is_flag=True,
    help="Include hidden files and folders",
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
def tree(dir_path: str, show_hidden: bool, save: bool, output: str) -> None:
    """DIR_PATH: Path to directory to be scanned"""

    scanner.build_tree(dir_path, show_hidden, save, output)


@fm.command()
@click.argument("dir_path", type=click.STRING)
@click.option(
    "-h",
    "--hidden",
    "show_hidden",
    is_flag=True,
    help="Include hidden files and folders",
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
def pretty_tree(dir_path: str, show_hidden: bool, save: bool, output: str) -> None:
    """DIR_PATH: Path to directory to be scanned"""

    scanner.build_pretty_tree(dir_path, show_hidden, save, output)


#############################################################
@fm.command()
@click.argument("dir_path", type=click.STRING)
@click.argument("name", type=click.STRING)
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
    """
    Search by NAME inside DIR_PATH
    """
    if recursively:
        scanner.search_recursively(dir_path, name, save, output)
    else:
        scanner.search(dir_path, name, save, output)


#############################################################
@fm.command()
@click.argument("dir_path", type=click.STRING)
@click.argument("other_path", type=click.STRING)
@click.option(
    "-h",
    "--hidden",
    "include_hidden",
    is_flag=True,
    help="Include hidden files and folders",
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
    """
    Compare DIR_PATH to OTHER_PATH
    """
    if short and one_line:
        raise click.BadParameter("Mutually exclusive flags: 'short' and 'oneline'")
    scanner.compare_directories(
        dir_path, other_path, include_hidden, short, one_line, recursively, save, output
    )


#############################################################
# ### organize ###
@fm.command()
@click.argument("dir_path", type=click.STRING)
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
    help="Move all files to target directories inside parent folder. (Used with --recursively flag)",
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
    """
    Organize files by extension/type inside DIR_PATH
    """
    if recursively:
        organizer.organize_files_recursively(
            dir_path, exclude, exclude_dir, flat, show_hidden, backup, archive_format, save, output
        )
    else:
        organizer.organize_files(dir_path, exclude, show_hidden, backup, archive_format, save, output)


#####################################
@fm.command()
@click.argument("dir_path", type=click.STRING)
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
    """
    Find and clean-up duplicate files inside a PATH
    """
    if recursively:
        organizer.handle_duplicate_files(
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
