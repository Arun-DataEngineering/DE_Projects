import logging

def fn_log_print(level, message):

    if level.upper() == "INFO":
        logging.info(message)

    elif level.upper() == "WARNING":
        logging.warning(message)

    elif level.upper() == "ERROR":
        logging.error(message)

    elif level.upper() == "DEBUG":
        logging.debug(message)

    print(message)