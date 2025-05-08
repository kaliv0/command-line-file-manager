import hashlib
import os
import shutil
from collections import defaultdict
from collections.abc import Generator
from logging import Logger

import click

from file_manager.logs import log_messages
from file_manager.logs.logger_factory import get_logger
from file_manager.utils import should_skip_hidden
from file_manager.utils.config import constants


BACKUP_FILE_NAME = ".bak"
SKIPPED_BACKUP_FILES = [".backup.tar.gz", ".backup.zip"]
TARGET_MAP = constants.TARGET_MAP


def organize_files(
    dir_path: str,
    exclude: str,
    config: str,
    show_hidden: bool,
    backup: bool,
    archive_format: str,
    save: bool,
    output: str,
    log: str,
) -> None:
    abs_dir_path, dir_list = _handle_dir_path(dir_path)
    logger = get_logger(output, save, log)
    is_reorganized = False

    if backup:
        _create_archive(abs_dir_path, archive_format)
    if config:
        # reassign config -> could be cleaner if classes were used
        global TARGET_MAP
        TARGET_MAP = _parse_config(config)

    exclude_list = exclude.split(",") if exclude else []
    for entry in dir_list:
        abs_entry_path = os.path.join(abs_dir_path, entry)
        if os.path.isfile(abs_entry_path):
            file_extension = _get_file_extension(entry)
            if (should_skip_hidden(show_hidden, entry)) or file_extension in exclude_list:
                logger.info(log_messages.SKIP_FILE.format(entry=entry))
                continue
            is_reorganized = _handle_entries(abs_dir_path, abs_entry_path, entry, file_extension, logger)

    if not is_reorganized:
        logger.info(log_messages.NOT_REORGANIZED)


################################
def organize_files_recursively(
    dir_path: str,
    exclude: str,
    exclude_dir: str,
    flat: bool,
    config: str,
    show_hidden: bool,
    backup: bool,
    archive_format: str,
    save: bool,
    output: str,
    log: str,
) -> None:
    abs_dir_path = os.path.abspath(dir_path)
    logger = get_logger(output, save, log)

    if backup:
        _create_archive(abs_dir_path, archive_format)
    if config:
        global TARGET_MAP
        TARGET_MAP = _parse_config(config)

    exclude_list = exclude.split(",") if exclude else []
    exclude_dir_list = exclude_dir.split(",") if exclude_dir else []
    if flat:
        root_dir = os.path.join(abs_dir_path, "")
        _handle_files_by_flattening_subdirs(
            abs_dir_path,
            "",
            root_dir,
            exclude_list,
            exclude_dir_list,
            show_hidden,
            logger,
            log,
        )
    else:
        _handle_files(abs_dir_path, "", exclude_list, exclude_dir_list, show_hidden, logger, log)


def _handle_files(
    parent_dir: str,
    subdir_path: str,
    exclude_list: list[str],
    exclude_dir_list: list[str],
    show_hidden: bool,
    logger: Logger,
    log_file: str,
) -> None:
    abs_dir_path = os.path.join(parent_dir, subdir_path)
    dir_list = os.listdir(abs_dir_path)

    logger.info(log_messages.INSIDE_DIR.format(abs_dir_path=abs_dir_path))
    nested_dirs = []
    is_reorganized = False
    has_skipped = False
    for entry in dir_list:
        abs_entry_path = os.path.join(abs_dir_path, entry)
        # handle files
        if os.path.isfile(abs_entry_path):
            if entry == log_file or entry in SKIPPED_BACKUP_FILES:
                continue
            file_extension = _get_file_extension(entry)
            if should_skip_hidden(show_hidden, entry) or file_extension in exclude_list:
                logger.info(log_messages.SKIP_FILE.format(entry=entry))
            else:
                is_reorganized = _handle_entries(abs_dir_path, abs_entry_path, entry, file_extension, logger)
        # list nested dirs
        elif os.path.isdir(abs_entry_path):
            # NB: skip hidden dirs -> don't create extra ".hidden" subdirs
            if _should_skip_dir(entry, exclude_dir_list, show_hidden):
                logger.info(log_messages.SKIP_DIR.format(entry=entry))
                has_skipped = True
                continue
            nested_dirs.append(abs_entry_path)

    if not (is_reorganized or has_skipped):
        logger.info(log_messages.NOT_REORGANIZED)

    # dive recursively to handle nested dirs
    for nested_dir in nested_dirs:
        _handle_files(
            abs_dir_path,
            nested_dir,
            exclude_list,
            exclude_dir_list,
            show_hidden,
            logger,
            log_file,
        )


def _handle_files_by_flattening_subdirs(
    parent_dir: str,
    subdir_path: str,
    root_dir: str,
    exclude_list: list[str],
    exclude_dir_list: list[str],
    show_hidden: bool,
    logger: Logger,
    log_file: str,
) -> None:
    abs_dir_path = os.path.join(parent_dir, subdir_path)
    dir_list = os.listdir(abs_dir_path)

    logger.info(log_messages.INSIDE_DIR.format(abs_dir_path=abs_dir_path))
    nested_dirs = []
    is_reorganized = False
    for entry in dir_list:
        abs_entry_path = os.path.join(abs_dir_path, entry)
        # handle files
        if os.path.isfile(abs_entry_path):
            if entry == log_file or entry in SKIPPED_BACKUP_FILES:
                continue
            file_extension = _get_file_extension(entry)
            if should_skip_hidden(show_hidden, entry) or file_extension in exclude_list:
                logger.info(log_messages.MOVE_FILE_TO_ROOT_DIR.format(entry=entry))
                shutil.move(abs_entry_path, os.path.join(root_dir, entry))
            else:
                is_reorganized = _handle_entries(root_dir, abs_entry_path, entry, file_extension, logger)
        # list nested dirs
        elif os.path.isdir(abs_entry_path):
            if _should_skip_dir(entry, exclude_dir_list, show_hidden):
                logger.info(log_messages.SKIP_DIR_AND_MOVE.format(entry=entry))
                shutil.move(abs_entry_path, os.path.join(root_dir, entry))
                continue
            nested_dirs.append(abs_entry_path)

    if not is_reorganized:
        logger.info(log_messages.NOT_REORGANIZED)

    # dive recursively to handle nested dirs
    for nested_dir in nested_dirs:
        _handle_files_by_flattening_subdirs(
            abs_dir_path,
            nested_dir,
            root_dir,
            exclude_list,
            exclude_dir_list,
            show_hidden,
            logger,
            log_file,
        )
    # flatten dir
    is_not_root_dir = abs_dir_path != root_dir
    is_not_one_level_nested_dir = os.path.join(os.path.dirname(abs_dir_path), "") != root_dir
    is_not_target_dir = os.path.basename(subdir_path) not in TARGET_MAP.values()
    if is_not_root_dir and (is_not_one_level_nested_dir or is_not_target_dir):
        logger.info(log_messages.REMOVE_DIR.format(abs_dir_path=abs_dir_path))
        os.rmdir(abs_dir_path)


def _should_skip_dir(entry: str, exclude_dir_list: list[str], show_hidden: bool) -> bool:
    return (not show_hidden and entry.startswith(".")) or entry in exclude_dir_list


def _parse_config(config: str) -> dict[str, str]:
    if not os.path.exists(config):
        raise click.ClickException(log_messages.MISSING_CONFIG_ERROR.format(path=config))
    if not os.path.getsize(config):
        raise click.ClickException(log_messages.EMPTY_CONFIG_ERROR.format(path=config))
    return _remap_config(_read_file(config))


def _read_file(config) -> dict[str, list[str]]:
    with open(config, "rb") as f:
        extension = _get_file_extension(config)
        match extension:
            case ".toml":
                import tomllib

                return tomllib.load(f)
            case ".json":
                import json

                return json.load(f)
            case ".yaml":
                import yaml

                return yaml.safe_load(f)
            case _:
                raise click.ClickException(log_messages.UNSUPPORTED_TYPE_ERROR.format(value=extension))


def _remap_config(config: dict[str, list[str]]) -> dict[str, str]:
    result = {}
    for k, v in config.items():
        for ext in v:
            if ext in result:
                raise click.ClickException(log_messages.DUPLICATE_ENTRY_ERROR.format(entry=ext))
            result[ext] = k

    result.setdefault("default", "other")
    result.setdefault("hidden", ".hidden")
    return result


#####################################
def handle_duplicate_files(
    dir_path: str,
    interactive: bool,
    show_hidden: bool,
    save: bool,
    output: str,
    log: str,
    backup: bool,
    archive_format: str,
) -> None:
    # BTW: could have used built-in filecmp.cmp but this is more fun
    abs_dir_path, dir_list = _handle_dir_path(dir_path)
    logger = get_logger(output, save, log)
    if backup:
        _create_archive(abs_dir_path, archive_format)

    content_map = _create_duplicate_map(abs_dir_path, dir_list, show_hidden, logger)
    _handle_duplicates(content_map, abs_dir_path, interactive, logger)


def handle_duplicate_files_recursively(
    dir_path: str,
    interactive: bool,
    show_hidden: bool,
    save: bool,
    output: str,
    log: str,
    backup: bool,
    archive_format: str | None = None,
    logger: Logger | None = None,
) -> None:
    abs_dir_path, dir_list = _handle_dir_path(dir_path)
    if not logger:
        logger = get_logger(output, save, log)
    logger.info(log_messages.INSIDE_DIR.format(abs_dir_path=abs_dir_path))

    if backup:
        _create_archive(abs_dir_path, archive_format)  # noqa

    content_map, subdir_list = _create_duplicate_map_and_subdir_list(
        abs_dir_path, dir_list, show_hidden, logger
    )
    # handle duplicates in current dir
    _handle_duplicates(content_map, abs_dir_path, interactive, logger)
    # dive recursively into nested subdirs
    logger.info(log_messages.DUPLICATE_DELIMITER)
    for subdir in subdir_list:
        handle_duplicate_files_recursively(
            subdir,
            interactive,
            show_hidden,
            save,
            output,
            log,
            backup=False,
            archive_format=None,
            logger=logger,
        )


def _create_duplicate_map(
    abs_dir_path: str, dir_list: list[str], show_hidden: bool, logger: Logger
) -> defaultdict[str, list[str]]:
    content_map = defaultdict(list[str])
    for entry in dir_list:
        abs_entry_path = os.path.join(abs_dir_path, entry)
        if os.path.isfile(abs_entry_path):
            _add_entry(entry, abs_entry_path, content_map, show_hidden, logger)
    return content_map


def _create_duplicate_map_and_subdir_list(
    abs_dir_path: str, dir_list: list[str], show_hidden: bool, logger: Logger
) -> tuple[defaultdict[str, list[str]], list[str]]:
    content_map = defaultdict(list[str])
    subdir_list = []
    for entry in dir_list:
        abs_entry_path = os.path.join(abs_dir_path, entry)
        if os.path.isfile(abs_entry_path):
            _add_entry(entry, abs_entry_path, content_map, show_hidden, logger)
        elif os.path.isdir(abs_entry_path):
            subdir_list.append(abs_entry_path)
    return content_map, subdir_list


def _add_entry(
    entry: str,
    abs_entry_path: str,
    content_map: defaultdict[str, list[str]],
    show_hidden: bool,
    logger: Logger,
) -> None:
    if should_skip_hidden(show_hidden, entry):
        logger.info(log_messages.SKIP_FILE.format(entry=entry))
        return

    with open(abs_entry_path, "rb") as f:
        sha = hashlib.sha1(f.read()).hexdigest()
    content_map[sha].append(entry)


def _handle_duplicates(
    content_map: defaultdict[str, list[str]],
    dir_path: str,
    interactive: bool,
    logger: Logger,
) -> None:
    duplicate_list = _transform_content_map(content_map)
    # display sorted map entries
    if not duplicate_list:
        logger.info(log_messages.NO_DUPLICATE_FILES.format(dir_path=dir_path))
        return
    logger.info(
        log_messages.LISTED_DUPLICATE_FILES.format(
            dir_path=dir_path,
            display_list="".join(_prepare_display_list(duplicate_list)),
        )
    )
    # clean-up files
    _merge_duplicates(dir_path, duplicate_list, interactive, logger)


def _transform_content_map(content_map: defaultdict[str, list[str]]) -> list[list[str]]:
    return [
        sorted(file_list)
        for file_list in content_map.values()
        # should contain more than elements with equal extensions
        if len(file_list) > 1 and len({_get_file_extension(entry) for entry in file_list}) == 1
    ]


def _prepare_display_list(duplicate_list: list[list[str]]) -> Generator[str]:
    for file_list in duplicate_list:
        for file in sorted(file_list):
            yield f"\t- {file}\n"
        yield log_messages.DUPLICATE_DELIMITER


def _merge_duplicates(
    abs_dir_path: str,
    duplicate_list: list[list[str]],
    interactive: bool,
    logger: Logger,
) -> None:
    for entry in duplicate_list:
        for idx, file in enumerate(entry):
            abs_file_path = os.path.join(abs_dir_path, file)
            if idx == 0:
                if interactive:
                    target_name = click.prompt(
                        text=log_messages.PRE_MERGE_PROMPT.format(entry=entry),
                        type=click.STRING,
                    )
                else:
                    target_name = file
                abs_target_path = os.path.join(abs_dir_path, target_name)
                logger.info(log_messages.MERGE_FILES.format(entry=entry, target_name=target_name))
                shutil.move(abs_file_path, abs_target_path)
            else:
                os.remove(abs_file_path)


# ### helpers ###
def _handle_dir_path(dir_path: str) -> tuple[str, list[str]]:
    abs_dir_path = os.path.abspath(dir_path)
    dir_list = os.listdir(dir_path)
    return abs_dir_path, dir_list


def _create_archive(abs_dir_path: str, archive_format: str) -> None:
    shutil.make_archive(
        base_name=os.path.join(abs_dir_path, BACKUP_FILE_NAME),
        format=archive_format,
        root_dir=os.path.dirname(abs_dir_path),
        base_dir=os.path.basename(abs_dir_path),
        verbose=True,
    )


def _handle_entries(
    abs_dir_path: str,
    abs_entry_path: str,
    entry: str,
    file_extension: str,
    logger: Logger,
) -> bool:
    if entry.startswith("."):
        target_dir_name = TARGET_MAP["hidden"]
    else:
        target_dir_name = TARGET_MAP.get(file_extension, TARGET_MAP["default"])

    # don't create identical path inside current one e.g. foo/bar -> foo/bar/bar
    if target_dir_name == os.path.basename(abs_dir_path):
        return False

    target_dir = os.path.join(abs_dir_path, target_dir_name)
    # don't try to move file into its own dir
    if target_dir == os.path.dirname(abs_entry_path):
        return False

    if not os.path.exists(target_dir):
        logger.info(log_messages.CREATE_DIR.format(target_dir=target_dir))
        os.makedirs(target_dir)
    logger.info(log_messages.MOVE_FILE.format(entry=entry, target_dir=target_dir))
    shutil.move(abs_entry_path, os.path.join(target_dir, entry))
    return True


def _get_file_extension(entry: str) -> str:
    return os.path.splitext(entry)[1]
