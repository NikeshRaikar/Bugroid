import subprocess
from pathlib import Path
from datetime import datetime

from config import (
    VIDEO_DIR,
    VIDEO_DURATION,
)




def record_video(
    camera_device,
    suffix,
    logger,
):
    output = (
        VIDEO_DIR
        / f"{datetime.now():%Y%m%d_%H%M%S}_{suffix}.mp4"
    )

    logger.info(
        "Recording %s",
        output,
    )

    subprocess.Popen(
        [
            "ffmpeg",
            "-y",
            "-t",
            str(VIDEO_DURATION),
            "-i",
            camera_device,
            str(output),
        ]
    )