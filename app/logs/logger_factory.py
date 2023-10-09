import logging

from app.logs.config import logger_types, log_output, log_messages


class LoggerFactory:
    @classmethod
    def get_logger(cls, logger_type: str, output_dir: str, save_output: bool) -> logging.Logger:
        match logger_type:
            case logger_types.BASIC:
                return cls._configure_logger(logger_types.BASIC, output_dir + log_output.FILES)
            case logger_types.CATALOG:
                return cls._configure_logger(logger_types.CATALOG, output_dir + log_output.CATALOG)
            case logger_types.RECURSIVE:
                return cls._configure_logger(
                    logger_types.RECURSIVE, output_dir + log_output.RECURSIVE_CATALOG
                )
            case logger_types.TREE:
                return cls._configure_logger(logger_types.TREE, output_dir + log_output.TREE)
            case logger_types.SEARCH:
                return cls._configure_logger(logger_types.SEARCH, output_dir + log_output.SEARCH)
            case logger_types.ORGANIZE:
                return cls._configure_organize_logger(
                    logger_types.ORGANIZE, save_output, output_dir + log_output.ORGANIZE
                )
            case logger_types.RECURSIVE_ORGANIZE:
                return cls._configure_organize_logger(
                    logger_types.ORGANIZE, save_output, output_dir + log_output.RECURSIVE_ORGANIZE
                )

    @staticmethod
    def _configure_logger(logger_name: str, output_file_name: str) -> logging.Logger:
        logger = logging.getLogger(logger_name)
        file_handler = logging.FileHandler(filename=output_file_name, mode="w")
        formatter = logging.Formatter(log_messages.LOG_FORMAT)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        return logger

    @staticmethod
    def _configure_organize_logger(
        logger_name: str, save_output: bool, output_file_name: str
    ) -> logging.Logger:
        logger = logging.getLogger(logger_name)
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(log_messages.LOG_FORMAT)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        if save_output:
            file_handler = logging.FileHandler(filename=output_file_name, mode="a")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        logger.setLevel(logging.INFO)
        return logger
