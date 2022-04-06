import logging


def init_logging():
    logging.basicConfig(
        filename="/var/log/webdisk/log.log",
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s',
        level=logging.DEBUG,
    )
