#!/bin/bash
# This script is developed by Nikesh Jagadeesh raikar from DQA1 Germany
# Contact : extnikesh.raikar@lgepartner.com

set -e
echo "Configuring LOGRoid : "
sudo mkdir -p /var/lib/logroid
sudo mkdir -p /var/log/logroid

sudo chown -R $USER:$USER /var/lib/logroid
sudo chown -R $USER:$USER /var/log/logroid

sudo chown -R 755 /var/lib/logroid/
sudo chown -R 755  /var/log/logroid/

sudo chmod +x /opt/logroid/usb_can_sync.sh

sudo systemctl daemon-reload
sudo systemctl enable android-logger.service
sudo systemctl start android-logger.service
sudo udevadm control --reload-rules
sudo udevadm trigger
echo "Logroid installed"

exit 0