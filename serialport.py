#!/usr/bin/python
import serial
#import syslog
import time
import serial
import time
port = "com4"
speed = 9600
valueToWrite = "r"
try:
    arduino = serial.Serial()
    arduino.port = "COM4"
    arduino.baudrate = 19200
    arduino.timeout = 1
    arduino.setDTR(False)
    arduino.setRTS(False)
    arduino.open()


#    time.sleep(2)
    print("Connection to " + port + " established succesfully!\n")
except Exception as e:
    print(e)

#Note: for characters such as 'a' I set data = b'a' to convert the data in bytes
#However the same thing does not work with numbers...
data = 0
for i in range(100):

    data = arduino.write(valueToWrite.encode())
    time.sleep(.2)
    out = arduino.readline()
    num = int(out.strip().decode()) & 0xffffffff
    print(num)
arduino.close()