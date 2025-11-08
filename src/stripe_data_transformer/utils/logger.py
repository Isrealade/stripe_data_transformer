import logging

def get_logger(name: str, debug: bool = False):
    logger = logging.getLogger(name)

    # Prevent logs from propagating to root logger
    # logger.propagate = False

    # Clear old handlers
    if logger.handlers:
        logger.handlers.clear()

    # Set logger level
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
