import serial
import time

# opens the serial connection
ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)

# buffer time for XBee to initialize
time.sleep(2)

# infinite loop
while True:
	ser.write(b'Hello, World from jacker1!\n')
	print("message sent")
	time.sleep(2)
