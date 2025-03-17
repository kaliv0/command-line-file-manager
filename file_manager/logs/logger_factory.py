import logging

from file_manager.logs.config import log_messages, log_output, logger_types


def get_logger(logger_type: str, output_dir: str, save_output: bool) -> logging.Logger:
    match logger_type:
        case logger_types.BASIC:
            return _configure_logger(logger_types.BASIC, save_output, output_dir, log_output.FILES)
        case logger_types.CATALOG:
            return _configure_logger(logger_types.CATALOG, save_output, output_dir, log_output.CATALOG)
        case logger_types.TREE:
            return _configure_logger(logger_types.TREE, save_output, output_dir, log_output.TREE)
        case logger_types.SEARCH:
            return _configure_logger(logger_types.SEARCH, save_output, output_dir, log_output.SEARCH)
        case logger_types.COMPARE:
            return _configure_logger(logger_types.COMPARE, save_output, output_dir, log_output.COMPARE)
        case logger_types.ORGANIZE:
            return _configure_logger(logger_types.ORGANIZE, save_output, output_dir, log_output.ORGANIZE)
        case logger_types.DEDUPLICATE:
            return _configure_logger(
                logger_types.DEDUPLICATE, save_output, output_dir, log_output.DEDUPLICATE
            )
        case _:
            return _configure_logger(logger_types.BASIC, save_output, output_dir, log_output.FILES)


def _configure_logger(logger_name: str, save_output: bool, output_dir: str, file_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(log_messages.LOG_FORMAT)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if save_output:
        file_handler = logging.FileHandler(filename=(output_dir + file_name), mode="a")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.setLevel(logging.INFO)
    return logger
