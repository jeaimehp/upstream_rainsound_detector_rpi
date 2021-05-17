#!/bin/bash
sudo systemctl status --no-pager sound-rain-monitoring-py.service >> /home/pi/upstreamrain/log/sensorservice-restsart.log
echo "Restarting" >>  /home/pi/upstreamrain/log/sensorservice-restsart.log

sudo systemctl stop sound-rain-monitoring-py.service
sleep 10
sudo systemctl start sound-rain-monitoring-py.service
