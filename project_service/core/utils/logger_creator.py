import logging


class LoggerCreator:
    """
    LoggerCreator is a class to create and config logger

    To create logger:
    logger = LoggerCreator(module_name, log_file_name, format_string).logger

    Use for log:
    logger.info(info_message)
    logger.debug(debug_message)
    logger.warning(warning_message)
    """

    def __init__(self, module_name, log_file_name, format_string, debug=True):
        self.logger = self._logger_config(module_name, log_file_name, format_string, debug=debug)

    @staticmethod
    def _logger_config(module_name, log_file_name, format_string, debug=True):
        logger = logging.getLogger(module_name)

        if debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        fh = logging.FileHandler(f'core/logs/{log_file_name}')
        formatter = logging.Formatter(format_string, datefmt='%m/%d/%Y %I:%M:%S %p')

        fh.setFormatter(formatter)
        logger.addHandler(fh)

        return logger
