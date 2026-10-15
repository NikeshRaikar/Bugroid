import subprocess


def device_connected():
    try:
        result = subprocess.run(
            ["adb", "get-state"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        return result.stdout.strip() == "device"

    except Exception:
        return False


def recover_adb(logger):
    logger.warning(
        "Recovering ADB"
    )

    subprocess.run(
        ["adb", "kill-server"],
        check=False,
    )

    subprocess.run(
        ["adb", "start-server"],
        check=False,
    )