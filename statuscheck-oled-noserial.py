#!/usr/bin/python

# Libraries
import time
import math
from grove.i2c import Bus
from grove_oled_display_128x64 import GroveOledDisplay128x64
from grove.adc import ADC

# Boot Sequence on Oled
display = GroveOledDisplay128x64()
display.set_cursor(0, 0)
display.puts('UPSTREAM:')
display.set_cursor(1,0)
display.puts('Rain Detector')
display.set_cursor(2,0)
display.puts('Booting....')
time.sleep(2)
display.clear()

# Sensor Check
print ("\n--- Status Check Started ---\n")
display.set_cursor(0, 0)
display.puts('Checking Sensors')


import smbus

bus = smbus.SMBus(1) # 1 indicates /dev/i2c-1
linecount = 2
grove_OLED = False
grove_RTC =  False
grove_ADC = False
hydreon_RG9 = False

# OLED and ADC check
print('--> ADC(Sound), OLED, and RTC Checks (I2C)')
for device in range(128):
      try:
         bus.read_byte(device)
         if hex(device) == '0x3c':
           display.set_cursor(linecount, 0)
           display.puts('OLED(0x3c) = OK')
           grove_OLED = True
           linecount += 1
           print('\nOLED @ ' + hex(device) + ' = Detected')
         elif hex(device) == '0x4':
           display.set_cursor(linecount, 0)
           display.puts('ADC(0x4) = OK')
           grove_Sound = True
           linecount += 1
           print('\nADC @ ' + hex(device) + ' = Detected')
           print ("Analog device using slot A0")
           print ("Detecting Sample Sound values")
           for i in xrange(5):
             print("Value {0}: {1}".format(i,ADC().read(0)))
             time.sleep(.3)
           print(" ")
         else:
           display.set_cursor(linecount, 0)
           display.puts('Unknown ' + hex(device) + '?')
           print('\nUnknown i2c Device @ ' + hex(device) + ' = Detected')
           linecount += 1
 
      except: # exception if read_byte fails
         pass

# RTC Check
import os
import re
rtccheck = os.popen("timedatectl |grep 'RTC\ time\|Failed'").read().strip()
print('')
print(rtccheck)
display.set_cursor(linecount, 0)
if len(rtccheck) < 1:
  display.puts('RTC Not Detected')
  grove_RTC = False
else:
  rtccheck = rtccheck.split()
  display.puts('RTC = OK')
  linecount += 1
  display.set_cursor(linecount, 0)
  display.puts(rtccheck[4]+' UTC')
  linecount += 1
  grove_RTC = True

# Rain Gauge Reset and Check
#import serial
#import time
#
#print ('\n--> RG9 Rain Gauge Check (UART)')
#ser = serial.Serial(
#    port='/dev/ttyAMA0',\
#    baudrate=9600,\
#    parity=serial.PARITY_NONE,\
#    stopbits=serial.STOPBITS_ONE,\
#    bytesize=serial.EIGHTBITS,\
#        timeout=0)
#
#
#ser.close()
#tries = 0
#while not ser.readable():
#  print("/dev/ttyAMA0 not open")
#  ser.close()
#  time.sleep(.3)
#  tries =+ 1
#  if tries > 20:
#    exit("Could not read serial port")
#
#
#
#
#ser.close()
#time.sleep(.10)
#ser.open()
#ser.flush()
#time.sleep(.10)
#ser.reset_input_buffer()
#time.sleep(.10)
#ser.reset_output_buffer()
#time.sleep(.10)
#
#
#ser.close()
#ser.open()
#ser.write('K\r\n'.encode())
#time.sleep(.3)
#count = 0
#line = ''
#pwrdays_count = 0
#while count < 7:
#  message = ser.readline()
#  if len(message) > 1:
#     line = line + message
#     if  message.endswith('\n'):
#       print (line)
#       if line.find('PwrDays') > -1:
#         pwrdays_count += 1
#       line = ''
#       count += 1
#          
#
#ser.close()
#if pwrdays_count > -1:
#  display.set_cursor(linecount, 0)
#  display.puts('RG9 = OK')
#  linecount += 1
#  hydreon_RG9 = True
#else:
#  display.set_cursor(linecount, 0)
#  display.puts('RG9 = Not Detected')
#  hydreon_RG9 = False

display.set_cursor(linecount, 0)
display.puts('RG9 = Unknown')

print ("--- Status Check Complete ---")
