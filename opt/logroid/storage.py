import shutil

from config import (
    BUGREPORT_DIR,
    LOGCAT_DIR,
    VIDEO_DIR,
    MIN_FREE_SPACE_GB,
)


def initialize_storage():
    for directory in (
        BUGREPORT_DIR,
        LOGCAT_DIR,
        VIDEO_DIR,
    ):
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )


def free_space_gb():
    usage = shutil.disk_usage(BUGREPORT_DIR)

    return usage.free / (1024**3)


def oldest_file():
    files = []

    for directory in (
        BUGREPORT_DIR,
        LOGCAT_DIR,
        VIDEO_DIR,
    ):
        files.extend(
            [
                f
                for f in directory.rglob("*")
                if f.is_file()
            ]
        )

    if not files:
        return None

    return min(
        files,
        key=lambda path: path.stat().st_mtime,
    )


def cleanup_storage(logger):
    while free_space_gb() < MIN_FREE_SPACE_GB:
        file_path = oldest_file()

        if not file_path:
            break

        logger.warning(
            "Deleting %s",
            file_path,
        )

        file_path.unlink(
            missing_ok=True,
        )