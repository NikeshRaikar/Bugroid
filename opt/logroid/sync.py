import shutil

from config import (
    BUGREPORT_DIR,
    LOGCAT_DIR,
    VIDEO_DIR,
    USB_BUGREPORT_DIR,
    USB_LOGCAT_DIR,
    USB_VIDEO_DIR,
    SYNC_INTERVAL,
)
from shutdown import shutdown_event
from usb import usb_available


def move_files(
    source,
    destination,
    logger,
):
    destination.mkdir(
        parents=True,
        exist_ok=True,
    )

    for file_path in source.glob("*"):

        if not file_path.is_file():
            continue

        target = (
            destination /
            file_path.name
        )

        try:
            shutil.move(
                str(file_path),
                str(target),
            )

            logger.info(
                "Transferred %s",
                file_path.name,
            )

        except Exception:
            logger.exception(
                "Failed to transfer %s",
                file_path,
            )


def sync_loop(logger):
    while not shutdown_event.is_set():

        if usb_available():

            move_files(
                BUGREPORT_DIR,
                USB_BUGREPORT_DIR,
                logger,
            )

            move_files(
                LOGCAT_DIR,
                USB_LOGCAT_DIR,
                logger,
            )

            move_files(
                VIDEO_DIR,
                USB_VIDEO_DIR,
                logger,
            )

        shutdown_event.wait(
            SYNC_INTERVAL,
        )