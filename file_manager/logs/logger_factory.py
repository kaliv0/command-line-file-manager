import logging
import os.path

from file_manager.logs import log_messages


def get_logger(output_dir: str, save_output: bool, log_name: str) -> logging.Logger:
    logger = logging.getLogger()
    stream_handler = logging.StreamHandler()
    stream_handler.terminator = ""
    formatter = logging.Formatter(log_messages.LOG_FORMAT)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if save_output:
        log_file = os.path.join(os.path.abspath(output_dir), log_name)
        if os.path.exists(log_file):
            os.remove(log_file)

        file_handler = logging.FileHandler(filename=log_file, mode="a")
        file_handler.terminator = ""
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.setLevel(logging.INFO)
    return logger
