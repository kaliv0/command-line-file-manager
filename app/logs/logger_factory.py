import logging

from app.logs import logger_types


FILES = "/list.txt"
CATALOG = "/catalog.txt"
RECURSIVE_CATALOG = "/recursive_catalog.txt"
TREE = "/tree.txt"
SEARCH = "/search.txt"
ORGANIZE = "/organize.txt"

LOG_FORMAT = "%(message)s"


class LoggerFactory:
    @classmethod
    def get_logger(cls, logger_type, output_dir):
        if logger_type == logger_types.BASIC:
            return cls._configure_logger(logger_types.BASIC, output_dir + FILES)
        elif logger_type == logger_types.CATALOG:
            return cls._configure_logger(logger_types.CATALOG, output_dir + CATALOG)
        elif logger_type == logger_types.RECURSIVE:
            return cls._configure_logger(logger_types.RECURSIVE, output_dir + RECURSIVE_CATALOG)
        elif logger_type == logger_types.TREE:
            return cls._configure_logger(logger_types.TREE, output_dir + TREE)
        elif logger_type == logger_types.SEARCH:
            return cls._configure_logger(logger_types.SEARCH, output_dir + SEARCH)
        elif logger_type == logger_types.ORGANIZE:
            return cls._configure_logger(logger_types.ORGANIZE, output_dir + ORGANIZE)

    @staticmethod
    def _configure_logger(logger_name, output_file_name):
        logger = logging.getLogger(logger_name)
        f_handler = logging.FileHandler(filename=output_file_name, mode="w")
        formatter = logging.Formatter(LOG_FORMAT)
        f_handler.setFormatter(formatter)
        logger.addHandler(f_handler)
        logger.setLevel(logging.INFO)
        return logger
