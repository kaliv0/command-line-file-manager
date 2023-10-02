from dir_scanner import DirScanner
from log import logger_types
from log.logger_factory import LoggerFactory

if __name__ == "__main__":
    target_dir = input()
    output_dir = input()
    logger = LoggerFactory.get_logger(logger_types.BASIC, output_dir)

    scanner = DirScanner(target_dir)
    scanner.scan_dir()
    subdir_list = scanner.scan_subdirs()
    files_list = scanner.scan_files()
    logger.info(files_list)

    catalog_logger = LoggerFactory.get_logger(logger_types.CATALOG, output_dir)
    catalog = scanner.build_catalog()
    catalog_logger.info(catalog)

    recursive_catalog_logger = LoggerFactory.get_logger(logger_types.RECURSIVE, output_dir)
    recursive_catalog = scanner.build_catalog_recursively()
    recursive_catalog_logger.info(recursive_catalog)
