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
ser.write('R\r\n'.encode())
time.sleep(.5)
message = ser.readline()
#time.sleep(.5)
print(message)

ser.close()
