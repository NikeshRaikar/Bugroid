import subprocess
from datetime import datetime

from adb_utils import (
    device_connected,
    recover_adb,
)
from config import LOGCAT_DIR
from shutdown import shutdown_event


def logcat_loop(logger):
    while not shutdown_event.is_set():

        if not device_connected():
            recover_adb(logger)
            shutdown_event.wait(5)
            continue

        filename = (
            LOGCAT_DIR
            / f"logcat_{datetime.now():%Y%m%d_%H%M%S}.log"
        )

        logger.info(
            "Starting logcat %s",
            filename,
        )

        try:
            with filename.open(
                "w",
                encoding="utf-8",
            ) as handle:

                subprocess.run(
                    ["adb", "logcat"],
                    stdout=handle,
                    stderr=subprocess.STDOUT,
                    timeout=3600,
                    check=False,
                )

        except subprocess.TimeoutExpired:
            logger.info(
                "Log rotation timeout"
            )