from pathlib import Path

USB_MOUNT = Path("/media/renault/android")

LOCAL_ROOT = Path("/var/lib/logroid")

BUGREPORT_DIR = LOCAL_ROOT / "bugreports"
LOGCAT_DIR = LOCAL_ROOT / "logcat"
VIDEO_DIR = LOCAL_ROOT / "videos"

USB_BUGREPORT_DIR = USB_MOUNT / "BugReport"
USB_LOGCAT_DIR = USB_MOUNT / "LogcatLogs"
USB_VIDEO_DIR = USB_MOUNT / "Videos"

BUTTON_PIN = 18
LED_PIN = 11

VIDEO_DURATION = 180

SYNC_INTERVAL = 60

MIN_FREE_SPACE_GB = 5