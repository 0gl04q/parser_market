import os
import logging


def create_log_directory(log_dir):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)


def setup_logger(name, log_dir='logging/parser_market', level=logging.INFO):

    create_log_directory(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.FileHandler(f'{log_dir}/{name}.log', mode='a')

    formatter = logging.Formatter('%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
