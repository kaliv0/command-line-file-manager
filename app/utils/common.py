from typing import Optional

from app.logs.logger_factory import LoggerFactory


def save_logs_to_file(
    output_dir: Optional[str], dir_path: str, message: str, logger_type: str
) -> None:
    if not output_dir:
        output_dir = dir_path
    LoggerFactory.get_logger(logger_type, output_dir, True).info(message)
