# Android Logger Service

> Production-grade Raspberry Pi based Android logging, bugreport collection, video capture, and store-and-forward synchronization framework for long-running validation and field testing.

---

# Overview

Android Logger Service is a resilient embedded Linux application designed to continuously collect Android diagnostic data regardless of USB availability.

Unlike the previous implementation which depended on a mounted USB storage device, this architecture follows a **store-and-forward model**:

1. All data is collected and stored locally.
2. Logging never stops when USB is disconnected.
3. Data remains safely queued on local storage.
4. When a USB device becomes available, data is automatically synchronized.
5. Successfully transferred files are removed from local storage.

This ensures uninterrupted data collection during:

- USB disconnects
- Power failures
- Device reboots
- Field testing
- Long-duration validation campaigns

---

# Key Features

## Continuous Operation

✅ Automatic startup after reboot

✅ Automatic service restart on failure

✅ Graceful shutdown

✅ Long-running service architecture

✅ Store-and-forward data collection

✅ No dependency on USB availability

---

## Android Diagnostics

✅ Continuous ADB Logcat Capture

✅ Android Bugreport Collection

✅ Automatic ADB Recovery

✅ Device Detection Monitoring

✅ Automatic Reconnection Handling

---

## Video Recording

✅ FPK Camera Recording

✅ CID Camera Recording

✅ Automatic Triggered Recording

✅ Timestamped Evidence Collection

---

## Data Synchronization

✅ Background USB Synchronization

✅ Automatic File Transfer

✅ Retry Until Successful

✅ Safe File Movement

✅ Power-Loss Recovery

---

## Data Protection

✅ Local Persistent Storage

✅ Disk Space Monitoring

✅ Automatic Cleanup

✅ Log Rotation

✅ Configurable Retention Policies

---

# Architecture

```text
                              Android Device
                                     │
                                     ▼
                        ┌──────────────────────────┐
                        │      Data Collection     │
                        │                          │
                        │ • Logcat                │
                        │ • Bugreport             │
                        │ • Video Recording       │
                        └────────────┬─────────────┘
                                     │
                                     ▼
                    ┌─────────────────────────────┐
                    │ Local Spool Storage         │
                    │                             │
                    │ /var/lib/android-logger     │
                    └────────────┬────────────────┘
                                 │
                                 ▼
                         Synchronization
                              Thread
                                 │
                   ┌─────────────┴─────────────┐
                   │                           │
            USB Missing                 USB Available
                   │                           │
                   ▼                           ▼
        Continue Collecting          Transfer Files
                   │                           │
                   └──────────► USB Storage ◄──┘
```

---

# Project Structure

```text
android-logger/
│
├── main.py
├── config.py
├── shutdown.py
├── logger_config.py
│
├── storage.py
├── usb.py
├── sync.py
├── adb_utils.py
│
├── bugreport.py
├── logcat.py
├── recording.py
│
├── requirements.txt
├── pyproject.toml
│
├── systemd/
│   └── android-logger.service
│
└── README.md
```

---

# Data Flow

## Logcat Collection

```text
ADB Device
     │
     ▼
Continuous Logcat Capture
     │
     ▼
/var/lib/android-logger/logcat
     │
     ▼
Sync Queue
     │
     ▼
USB Storage
```

---

## Bugreport Collection

```text
Button Press
     │
     ▼
ADB Bugreport
     │
     ▼
Local Storage
     │
     ▼
USB Synchronization
```

---

## Video Collection

```text
Button Press
     │
     ▼
FFmpeg Recording
     │
     ▼
Local Video Storage
     │
     ▼
USB Synchronization
```

---

# Local Storage Layout

All collected data is stored locally first.

```text
/var/lib/android-logger/
│
├── bugreports/
│   ├── 20261014_120000.zip
│   └── ...
│
├── logcat/
│   ├── logcat_20261014_120000.log
│   └── ...
│
├── videos/
│   ├── 20261014_120000_CID.mp4
│   ├── 20261014_120000_FPK.mp4
│   └── ...
│
└── app_logs/
```

---

# USB Storage Layout

```text
/media/renault2/android/
│
├── BugReport/
│
├── LogcatLogs/
│
└── Videos/
```

---

# How Store-and-Forward Works

## Scenario 1: USB Not Connected

```text
Logger Running
       │
       ▼
Collect Logs
       ▼
Store Locally
       ▼
Wait For USB
```

No data is lost.

---

## Scenario 2: USB Inserted Later

```text
USB Detected
      │
      ▼
Sync Thread Starts
      │
      ▼
Transfer Pending Files
      │
      ▼
Delete Local Copy
      │
      ▼
Continue Collection
```

---

## Scenario 3: USB Removed During Operation

```text
USB Removed
      │
      ▼
Synchronization Stops
      │
      ▼
Collection Continues Locally
      │
      ▼
USB Reinserted
      │
      ▼
Synchronization Resumes
```

---

# Threads

The application uses multiple worker threads.

## BUGREPORT Thread

Responsibilities:

- Monitor GPIO button
- Generate bugreports
- Trigger video recordings

---

## LOGCAT Thread

Responsibilities:

- Monitor Android device
- Continuously capture logcat
- Recover ADB failures

---

## SYNC Thread

Responsibilities:

- Monitor USB storage
- Transfer pending files
- Clean synchronization queue

---

# Startup Sequence

```text
Boot
 │
 ▼
systemd
 │
 ▼
Android Logger Service
 │
 ▼
Create Storage Directories
 │
 ▼
Start Worker Threads
 │
 ▼
Begin Logging
 │
 ▼
Wait For USB (optional)
```

USB is NOT required for startup.

---

# Automatic Recovery

## ADB Recovery

When device communication is lost:

```text
adb kill-server
adb start-server
```

is executed automatically.

---

## Service Recovery

If the process crashes:

```ini
Restart=always
RestartSec=10
```

systemd automatically restarts the service.

---

## Reboot Recovery

```text
Power Failure
      │
      ▼
System Reboots
      │
      ▼
Service Starts Automatically
      │
      ▼
Pending Files Still Available
      │
      ▼
Synchronization Continues
```

---

# Disk Space Protection

The service continuously monitors free space.

When available storage falls below:

```python
MIN_FREE_SPACE_GB = 5
```

the oldest synchronized files are deleted first.

Benefits:

- Prevents SD card exhaustion
- Avoids system instability
- Maintains continuous logging

---

# Logging

Application logs are stored separately from collected data.

Location:

```text
/var/log/android-logger/
```

Example:

```text
android_logger.log
android_logger.log.2026-10-13
android_logger.log.2026-10-12
```

---

# Log Rotation

Automatic daily log rotation:

```python
TimedRotatingFileHandler
```

Configuration:

```text
Rotate Daily
Retain 30 Days
UTF-8 Encoding
Automatic Cleanup
```

---

# GPIO Configuration

| Component | Pin |
|------------|------|
| LED | 11 |
| Button | 18 |

Operation:

1. User presses button
2. LED turns on
3. FPK recording starts
4. CID recording starts
5. Android bugreport generated
6. Files stored locally
7. Files synchronized later

---

# Installation

## System Dependencies

```bash
sudo apt update

sudo apt install -y \
    python3 \
    python3-pip \
    adb \
    ffmpeg
```

---

## Python Dependencies

```bash
pip install -r requirements.txt
```

---

## Create Directories

```bash
sudo mkdir -p /var/lib/android-logger
sudo mkdir -p /var/log/android-logger
```

---

## Deploy Application

```bash
sudo mkdir -p /opt/android-logger

sudo cp -r . \
/opt/android-logger/
```

---

# Systemd Installation

Copy service:

```bash
sudo cp \
systemd/android-logger.service \
/etc/systemd/system/
```

Reload:

```bash
sudo systemctl daemon-reload
```

Enable:

```bash
sudo systemctl enable android-logger
```

Start:

```bash
sudo systemctl start android-logger
```

Verify:

```bash
sudo systemctl status android-logger
```

---

# Monitoring

Realtime logs:

```bash
journalctl -u android-logger -f
```

Application log:

```bash
tail -f \
/var/log/android-logger/android_logger.log
```

---

# Development Commands

## Run

```bash
python main.py
```

## Ruff

```bash
ruff check .
```

## Format

```bash
ruff format .
```

## Pylint

```bash
pylint .
```

---

# Reliability Goals

| Metric | Target |
|----------|----------|
| Power-Loss Recovery | Automatic |
| USB Disconnect Recovery | Automatic |
| USB Reconnect Recovery | Automatic |
| Data Collection Without USB | Supported |
| Reboot Recovery | Automatic |
| Service Failure Recovery | Automatic |
| Log Retention | Configurable |
| ADB Recovery | Automatic |

---

# Future Enhancements

Planned improvements:

- Thread watchdog auto-restart
- Camera health monitoring
- Web dashboard
- REST API
- Prometheus metrics
- Grafana dashboards
- CAN logging integration
- Automotive Ethernet logging
- Crash dump collection
- OTA update support
- Multi-device Android support

---

# License

Internal Use Only

Confidential and Proprietary

---

# Author

Nikesh Jagadeesh Raikar

LGEVG

Android Logger Service

Resilient Store-and-Forward Logging Framework for Android Validation Systems