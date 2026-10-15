import os

from config import USB_MOUNT


def usb_available():
    return os.path.ismount(
        str(USB_MOUNT),
    )