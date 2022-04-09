import logging


def init_logging():
    try:
        import config

        log_file = config.LOG_FILE
    except Exception:
        log_file = "/var/log/webdisk/log.log"

    logging.basicConfig(
        filename=log_file,
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s',
        level=logging.DEBUG,
    )
