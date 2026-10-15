import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

LOG_DIR = Path("/var/log/logroid")


def get_logger():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("android_logger")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | "
        "%(threadName)s | %(message)s"
    )

    handler = TimedRotatingFileHandler(
        LOG_DIR / "android_logger.log",
        when="midnight",
        backupCount=30,
        encoding="utf-8",
    )

    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(console)

    return logger