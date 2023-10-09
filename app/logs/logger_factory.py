import logging

from app.logs import logger_types


FILES = "/list.txt"
CATALOG = "/catalog.txt"
RECURSIVE_CATALOG = "/recursive_catalog.txt"
TREE = "/tree.txt"
SEARCH = "/search.txt"
ORGANIZE = "/organize.txt"
RECURSIVE_ORGANIZE = "/organize_recursively.txt"

LOG_FORMAT = "%(message)s"


class LoggerFactory:
    @classmethod
    def get_logger(cls, logger_type: str, output_dir: str) -> logging.Logger:
        match logger_type:
            case logger_types.BASIC:
                return cls._configure_logger(logger_types.BASIC, output_dir + FILES)
            case logger_types.CATALOG:
                return cls._configure_logger(logger_types.CATALOG, output_dir + CATALOG)
            case logger_types.RECURSIVE:
                return cls._configure_logger(logger_types.RECURSIVE, output_dir + RECURSIVE_CATALOG)
            case logger_types.TREE:
                return cls._configure_logger(logger_types.TREE, output_dir + TREE)
            case logger_types.SEARCH:
                return cls._configure_logger(logger_types.SEARCH, output_dir + SEARCH)
            case logger_types.ORGANIZE:
                return cls._configure_organize_logger(logger_types.ORGANIZE, output_dir + ORGANIZE)
            case logger_types.RECURSIVE_ORGANIZE:
                return cls._configure_organize_logger(logger_types.ORGANIZE, output_dir + RECURSIVE_ORGANIZE)

    @staticmethod
    def _configure_logger(logger_name: str, output_file_name: str) -> logging.Logger:
        logger = logging.getLogger(logger_name)
        file_handler = logging.FileHandler(filename=output_file_name, mode="w")
        formatter = logging.Formatter(LOG_FORMAT)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        return logger
    
    @staticmethod
    def _configure_organize_logger(logger_name: str, save_output: bool, output_file_name: str) -> logging.Logger:
        logger = logging.getLogger(logger_name)
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(LOG_FORMAT)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        if save_output:
            file_handler = logging.FileHandler(filename=output_file_name, mode="a")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        logger.setLevel(logging.INFO)
        return logger
    
    
 
