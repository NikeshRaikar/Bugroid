#!/bin/bash

# Device name passed by udev (e.g., sda1)
DEVICE=$1
MOUNT_POINT="/mnt/usb_$DEVICE"
LOCAL_ROOT="/var/lib/logroid"
VIDEO_LOGS="$LOCAL_ROOT/videos"
BUGREPORT_LOGS="$LOCAL_ROOT/bugreports"
LOGCAT_LOGS="$LOCAL_ROOT/logcat"


# Ensure we are dealing with a valid block device
if [ -z "$DEVICE" ]; then
    exit 1
fi

# Create mount point and mount the USB
mkdir -p "$MOUNT_POINT"
mount "/dev/$DEVICE" "$MOUNT_POINT"
if [ $? -ne 0 ]; then
    # Exit silently if mount fails (e.g., unsupported filesystem)
    rmdir "$MOUNT_POINT"
    exit 1
fi

# Enable nullglob so empty directories don't return the literal wildcard string
shopt -s nullglob
VIDEO=("$VIDEO_LOGS"/*.mp4)
LOGCAT=("$LOGCAT_LOGS"/*.log)
BUGREPORT=("$BUGREPORT_LOGS"/*.zip)


# Check if there are actually logs to move
if [ ${#VIDEO[@]} -eq 0 ] && [ ${#LOGCAT[@]} -eq 0 ] && [ ${#BUGREPORT[@]} -eq 0 ]; then
    # No logs found, unmount and exit
    umount "$MOUNT_POINT"
    rmdir "$MOUNT_POINT"
    exit 0
fi

# Stop loggers temporarily so we can safely move the active files
systemctl stop android-logger.service

# Create a timestamped directory on the USB to prevent file collisions
DEST_DIR="$MOUNT_POINT/combined_logs_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$DEST_DIR"

# Move the CAN logs to the USB if they exist
if [ ${#VIDEO[@]} -gt 0 ]; then
    mv "${VIDEO[@]}" "$DEST_DIR/"
fi

if [ ${#LOGCAT[@]} -gt 0 ]; then
    mv "${LOGCAT[@]}" "$DEST_DIR/"
fi

if [ ${#BUGREPORT[@]} -gt 0 ]; then
    mv "${BUGREPORT[@]}" "$DEST_DIR/"
fi



# Restart loggers to start fresh captures
systemctl start android-logger.service


# Flush filesystem buffers to guarantee data is physically written to the USB
sync

# Safely unmount and clean up
umount "$MOUNT_POINT"
rmdir "$MOUNT_POINT"
