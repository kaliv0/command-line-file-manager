import logging

from app.logs import logger_types


class LoggerFactory:
    FILES = "/files_list.txt"
    CATALOG = "/catalog.txt"
    RECURSIVE_CATALOG = "/recursive_catalog.txt"
    TREE = "/tree.txt"

    @classmethod
    def get_logger(cls, logger_type, output_dir):
        if logger_type == logger_types.BASIC:
            return cls._configure_logger(
                logger_types.BASIC, output_dir + cls.FILES
            )
        elif logger_type == logger_types.CATALOG:
            return cls._configure_logger(
                logger_types.CATALOG, output_dir + cls.CATALOG
            )
        elif logger_type == logger_types.RECURSIVE:
            return cls._configure_logger(
                logger_types.RECURSIVE, output_dir + cls.RECURSIVE_CATALOG
            )
        elif logger_type == logger_types.TREE:
            return cls._configure_logger(
                logger_types.TREE, output_dir + cls.TREE
            )

    @staticmethod
    def _configure_logger(logger_name, output_file_name):
        logger = logging.getLogger(logger_name)
        # s_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(filename=output_file_name, mode="w")

        formatter = logging.Formatter("%(message)s")
        # s_handler.setFormatter(formatter)
        f_handler.setFormatter(formatter)

        # logger.addHandler(s_handler)
        logger.addHandler(f_handler)

        logger.setLevel(logging.INFO)
        return logger
