#!/bin/bash
python /home/pi/upstreamrain/statuscheck-oled.py &
sleep 15
ps -elf|grep upstreamrain|grep python|awk '{print "kill "$4}'|bash

python /home/pi/upstreamrain/statuscheck-oled.py
SENSORLOGCHECK=$(tail -n1 /home/pi/upstreamrain/log/sensorstatus-$(date +"%Y%m%d").log)
echo $SENSORLOGCHECK
if [ "$SENSORLOGCHECK" == "OK" ]; then
       echo "Starting to record readings"
       sudo systemctl start sound-rain-monitoring-py.service
fi
 
sudo systemctl status sound-rain-monitoring-py.service
