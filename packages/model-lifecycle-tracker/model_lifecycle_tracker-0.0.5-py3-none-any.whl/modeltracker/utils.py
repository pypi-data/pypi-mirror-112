import logging

def get_logger(log_level=logging.DEBUG, modifier=""):
    """
    Jacques' personal logger
    get a logger that prints to a log_file, and to stdout/terminal. Is root logger so returns nothing
    :param log_file:
    :param log level for logger
    """


    formatter = logging.Formatter(
        '%(asctime)s [{}] %(levelname)s %(module)s - %(funcName)s: %(message)s'.format(modifier))
    log = logging.getLogger()
    log.setLevel(log_level)

    if len(log.handlers) > 0:
        log.handlers = []

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)
    return log
