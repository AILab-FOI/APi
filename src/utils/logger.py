import logging


def setup_logger(name: str):
    """
    Setup the logger for the given name.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Check if the logger already has handlers (to avoid duplicate logs)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Custom formatter to prepend param_value
        formatter = logging.Formatter(f"[{name}] %(message)s")
        ch.setFormatter(formatter)

        logger.addHandler(ch)

    return logger
