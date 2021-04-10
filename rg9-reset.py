import serial
import time

ser = serial.Serial(
    port='/dev/ttyAMA0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

ser.close()
ser.open()
ser.write('K\r\n'.encode())
time.sleep(.3)
count = 0
line = ''
while count < 7:
  message = ser.readline()
  if len(message) > 1:
    line = line + message
    if  message.endswith('\n'):
      print (line)
      line = ''
      count += 1
      #print (count)

ser.close()
