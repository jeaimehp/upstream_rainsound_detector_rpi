#!/bin/bash
sudo cp pi.cron /var/spool/cron/crontabs/pi
sudo systemctl restart cron
sudo systemctl status cron
