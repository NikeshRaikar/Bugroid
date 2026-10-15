import subprocess
from datetime import datetime

from RPi import GPIO

from adb_utils import device_connected
from config import (
    BUTTON_PIN,
    LED_PIN,
    BUGREPORT_DIR,
)
from recording import record_video
from shutdown import shutdown_event


def bugreport_loop(logger):
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(
        LED_PIN,
        GPIO.OUT,
    )

    GPIO.setup(
        BUTTON_PIN,
        GPIO.IN,
    )

    while not shutdown_event.is_set():

        GPIO.wait_for_edge(
            BUTTON_PIN,
            GPIO.FALLING,
            bouncetime=300,
        )

        GPIO.output(
            LED_PIN,
            GPIO.HIGH,
        )

        if not device_connected():
            continue

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        record_video(
            "/dev/video0",
            "FPK",
            logger,
        )

        record_video(
            "/dev/video4",
            "CID",
            logger,
        )

        output = (
            BUGREPORT_DIR /
            f"{timestamp}.zip"
        )

        subprocess.run(
            [
                "adb",
                "bugreport",
                str(output),
            ],
            timeout=900,
            check=False,
        )

        GPIO.output(
            LED_PIN,
            GPIO.LOW,
        )

    GPIO.cleanup()