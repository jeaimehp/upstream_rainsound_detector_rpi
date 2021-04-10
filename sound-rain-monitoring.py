#!/usr/bin/python
###################################################################################################
#  Program Name: (UPSTREAM) sound and rain monitor
#  Written By: Je'aime Powell
#  Created on: 4/10/21
#  Purpose: Collect and output the readings from a 
#     RG-9 (UART) rain gauge and sound sensor.
#
#  Tested Devices and Connections:
#      - Raspberry Pi Model 3B+
#            Ref: https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/
#      - Grove Base Hat for RPi Zero (SEEED Studios) 
#            Ref: https://wiki.seeedstudio.com/Grove_Base_Hat_for_Raspberry_Pi_Zero/
#            --> Analog to Digital Converter 12-bit 6 Channel (ADC=STM32F030x6)  (i2c - 0x40)
#                  * Grove UART port connect to the GPIO14(UART0 TX) and GPIO15(UART0 RX)
#      - Grove Sound Sensor (L358 Amplifier) (Analog Grove A0)
#            Ref:  https://wiki.seeedstudio.com/Grove-Sound_Sensor/
#      - Grove - DS1307 RTC (i2c - 0x68)
#            Ref: https://wiki.seeedstudio.com/Grove-RTC/
#      - Grove OLED Display 0.96" (SSD1308) (i2c - 0x3c)
#            Ref: https://wiki.seeedstudio.com/Grove-OLED_Display_0.96inch/
#      - Hydreon Rain Gauge RG-9 (UART - /dev/ttyAMA0)
#            Ref: https://www.seeedstudio.com/Rain-Gauge-RG-9-p-4744.html
#            Ref: https://rainsensors.com/rg-9
####################################################################################################
#############
# LIBRARIES #
#############

## Standard Libraries
import time
import math
import os
import datetime

#OLED Display
from grove.i2c import Bus
from grove_oled_display_128x64 import GroveOledDisplay128x64

## Grove Hat with ADC
from grove.adc import ADC
import smbus


## RG-9 UART Communications
import serial

##############
# Setup Code #
##############

# UART (Serial) Port Object for RG-9 Communications
ser = serial.Serial(
    port='/dev/ttyAMA0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

# Sound Sensor Grove Connected Port
sound_Pin = 0 # Port A0


# OLED Object Initialization
display = GroveOledDisplay128x64()
display.clear()
display.set_cursor(0, 0)
display.puts('Sampling Started')
## Variable to track position on Display
linecount_Display = 1

# Printing Initiazation Text on StdOut and Display
print("Sensor recordings started @ {}".format(datetime.datetime.utcnow()))
display.set_cursor(linecount_Display, 0)
display.puts(datetime.datetime.utcnow().strftime("%m/%d/%y %H:%M"))
linecount_Display += 2

###################
# Sensor Settings #
###################

# Setting key pair list creation
sensor_Settings = []

# No Rain Testing and Collection Interval - Samples/second
norain_Interval = 5 #seconds
## Add Value to the Sensor Settings keypair list
sensor_Settings.append({'norain_Interval':norain_Interval})

# Raining Data Collection Interval - Samples/second
rain_Interval = .5 #seconds
## Add Value to the Sensor Settings keypair list
sensor_Settings.append({'rain_Interval' :rain_Interval})

# What level of rain to increase collection times
rain_Sensitivity = 1 
# 0 = Dry, [1 = Rain Drops], 2 = Very Light, 3 = Medium Light, 4 = Medium, 5 = Medium Heavy, 6 = Heavy, 7 = Violent
# Ref: https://files.seeedstudio.com/wiki/Optical_Rain_Gauge_RG-9/2020.11.23-rg-9_instructions.pdf
## Add Value to the Sensor Settings keypair list
sensor_Settings.append({'rain_Sensitivity':rain_Sensitivity})

# Rain or Norain Status
rain_Status = False
## Add Value to the Sensor Settings keypair list
sensor_Settings.append({'rain_Status':rain_Status})

# Varible for Count of samples since last started
sample_Count = 0
## Add Value to the Sensor Settings keypair list
sensor_Settings.append({'sample_Count':sample_Count})

# Sensor Settings List Test Code
#print(sensor_Settings[0]['norain_Interval'])

# Print Sensor Setting to StdOut and Display
print('Sensor Settings:')
for key in sensor_Settings:
  print(key)
display.set_cursor(linecount_Display, 0)
display.puts("Sensitivity: " + str(sensor_Settings[2]['rain_Sensitivity']))
linecount_Display += 1
display.set_cursor(linecount_Display, 0)
display.puts("Rain: " + str(sensor_Settings[3]['rain_Status']))
linecount_Display += 1
display.set_cursor(linecount_Display, 0)
display.puts("Current Count: ")
linecount_Display += 1
display.set_cursor(linecount_Display, 0)
display.puts(str(sensor_Settings[4]['sample_Count']))

# Test/Debug OLED Redraw Line
#time.sleep(3)
#display.set_cursor(linecount_Display-1, 0)
#display.puts("JHP " + str(sensor_Settings[4]['sample_Count']))

###################
#    Functions    #
###################

def rain_Sample():
  ser.close()
  ser.open()
  ser.write('R\r\n'.encode())
  time.sleep(.3)
  message = ser.readline()
  #time.sleep(.5)
  ser.close()
  #Function Output Debug
  #print(message)
  return message[2]

def sound_Sample():
  sound_Value =  ADC().read(sound_Pin)
  #Function Output Debug
  #print(sound_Value)
  return sound_Value


###################
# Loop - Sampling #
###################
while sensor_Settings[4]['sample_Count'] < 50: # Dev Loop
#while True: # Production Loop
  #if rain_Status:
    
   # time.sleep(rain_Interval)
  rg_Value = int(rain_Sample())
  print('{},{},{}'.format(datetime.datetime.utcnow().strftime('%s'),sound_Sample(),rg_Value))
  sensor_Settings[4]['sample_Count'] += 1

  #Checks if Rain detected and sets rain_Status 
  if rg_Value > rain_Sensitivity:
    sensor_Settings[3]['rain_Status'] = True
    display.set_cursor(linecount_Display-2, 0)
    display.puts("Rain:       ")
    display.set_cursor(linecount_Display-2, 0)
    display.puts("Rain: " + str(sensor_Settings[3]['rain_Status']))
  else:
    sensor_Settings[3]['rain_Status'] = False
    display.set_cursor(linecount_Display-2, 0)
    display.puts("Rain: " + str(sensor_Settings[3]['rain_Status']))

  # Updates the OLED Sample Count display every 5 Samples
  if sensor_Settings[4]['sample_Count'] % 5 == 0:
    display.set_cursor(linecount_Display, 0)
    display.puts(str(sensor_Settings[4]['sample_Count']))

  # Sample Delay Option
  if sensor_Settings[3]['rain_Status']:
    time.sleep(sensor_Settings[1]['rain_Interval'])
  else:
    time.sleep(sensor_Settings[0]['norain_Interval'])

