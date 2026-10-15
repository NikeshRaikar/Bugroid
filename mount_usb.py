import os
import subprocess
import time
from datetime import datetime
from subprocess import PIPE, Popen
from threading import Lock, Thread

from RPi import GPIO

led_pin = 11  # Board pin 1
but_pin = 18  # Board pin 18
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(led_pin, GPIO.OUT)  # LED pin set as output
# GPIO.setup(but_pin, GPIO.IN)


def get_time():
    return datetime.now().strftime("_%Y-%m-%d_%H-%M-%S")


def delete_old_files():
    now = time.time()
    if get_usb_state():
        bugreport_path = "/media/renault2/android/BugReport"
        logcat_path = "/media/renault2/android/LogcatLogs"
        path = [bugreport_path, logcat_path]
        for i in path:
            for f in os.listdir(i):
                b = os.path.join(i, f)
                if os.stat(b).st_mtime < now - 7 * 86400:
                    if os.path.isfile(b):
                        os.remove(b)
                        print(f)
                else:
                    print(f"{get_time()}:  No files are older the 7 days")


def cid_record():
    while True:
        if get_usb_state():
            try:
                file = datetime.now().strftime("_%Y-%m-%d_%H-%M-%S")
                os.system(
                    f"ffmpeg -t 180 -i /dev/video0 /media/renault2/android/LogcatLogs/{file}_videotest_FPK.mp4",
                )
            except Exception as err:
                print(err)

        else:
            print(f"{get_time()}: USB not connected")


def fpk_record():
    print("FPK Record")
    while True:
        if get_usb_state():
            try:
                file = datetime.now().strftime("_%Y-%m-%d_%H-%M-%S")
                os.system(
                    f"ffmpeg -t 180 -i /dev/video4 /media/renault2/android/LogcatLogs/{file}_videotest_CID.mp4"
                )
            except Exception as err:
                print(err)
        else:
            print(f"{get_time()}: USB not connected")


def check_device_connected(command):
    process = Popen(command.split(), stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    lines = stdout.decode().splitlines()
    if len(lines) > 2:
        return True
    else:
        return False


def bugreport():
    while True:
        try:
            GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme#16FF27
            GPIO.setup(led_pin, GPIO.OUT)  # LED pin set as output
            GPIO.setup(but_pin, GPIO.IN)  # button pin set as input.
            GPIO.output(led_pin, GPIO.LOW)
            GPIO.wait_for_edge(but_pin, GPIO.FALLING)
            GPIO.output(led_pin, GPIO.HIGH)
            print(
                f"{get_time()}: Button Pressed!, Trying to generate bugreport if USB and Device is connected"
            )
            filetime = get_time()
            if get_usb_state():
                try:
                    if check_device_connected("adb devices"):
                        # ffmpeg -f pulse -ac 2 -i default -f v4l2 -i /dev/video0 -t 00:00:20 -vcodec libx264 dev/video0 /media/renault2/android/LogcatLogs/output.mp4
                        # original command : "ffmpeg -f pulse -ac 2 -t 180 -i /dev/video0 /media/renault2/android/LogcatLogs/_videotest_FPK_whitelight.mp4"
                        subprocess.Popen(
                            f"ffmpeg -t 180 -i /dev/video0 /media/renault2/android/LogcatLogs/{filetime}_videotest_FPK_whitelight.mp4",
                            shell=True,
                        )
                        subprocess.Popen(
                            f"ffmpeg -t 180 -i /dev/video4 /media/renault2/android/LogcatLogs/{filetime}_videotest_CID_bluelight.mp4",
                            shell=True,
                        )
                        os.system(
                            f"adb bugreport /media/renault2/android/BugReport/{filetime}.raw"
                        )
                        print(f"{get_time()} : Bugreport generated")
                    else:
                        print(f"{get_time()} : Button Pressed!, Devices not connected")
                    time.sleep(0.5)
                except Exception as err:
                    print(err)
                finally:
                    print(f"{get_time()} :cleaning GPIO Pins")
                    GPIO.cleanup()  # cleanup all GPIOs
            else:
                print(f"{get_time()} : Button Pressed!, USB not connected")
                GPIO.cleanup()  # cleanup all GPIOs
        except Exception as err:
            print(f"{get_time()} {err}: cleaning GPIO Pins")


def logcat():
    while True:
        if get_usb_state() and check_device_connected("adb devices"):
            try:
                filetime = get_time()
                os.system(
                    f"adb logcat -m 50000 >> /media/renault2/android/LogcatLogs/{filetime}.raw"
                )
                os.system("adb logcat -b all -c")
            except Exception as err:
                print(f"{get_time()} : {err}")
        else:
            print(f"{get_time()} : Logcat  ::::  >  USB or device not connected")


def get_usb_state():
    ret = subprocess.run(["df", "-h"], capture_output=True)
    if "/dev/sda1" in ret.stdout.decode():
        print(f"{get_time()} : checking mounted drive point")
        if os.path.ismount("/media/renault2/android"):
            print(f"{get_time()} : get_usb_state() :::: USB Mounted")
            return True

    else:
        return False


mutex = Lock()
cid_thread = Thread(target=cid_record)
cid_thread.name = "CID"
fpk_thread = Thread(target=fpk_record)
fpk_thread.name = "FPK"
bug_thread = Thread(target=bugreport)
bug_thread.name = "BUG"
logcat_thread = Thread(target=logcat)
logcat_thread.name = "LOGCAT"


if __name__ == "__main__":
    # cid_thread.start()
    # fpk_thread.start()
    delete_old_files()
    bug_thread.start()
    logcat_thread.start()

    # cid_thread.join()
    # fpk_thread.join()
    bug_thread.join()
    logcat_thread.join()
