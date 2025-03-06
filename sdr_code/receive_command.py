import serial

# opens serial connection
ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)

# infinite loop
while True:
	data = ser.readline().decode('utf-8').strip()
	if data:
		print(f"recieved: {data}")
