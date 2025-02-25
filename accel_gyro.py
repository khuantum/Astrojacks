import math
import time
import csv
from gpiozero import Button
import smbus2
from datetime import datetime

# setting up the buttom
button = Button(4)

# setting up i2c for accel
ACCEL_ADDR = 0x68
bus = smbus2.SMBus(1)

# initializing accel
bus.write_byte_data(ACCEL_ADDR, 0x6B, 0)

def read_accel():
	def read_word(reg):
		high = bus.read_byte_data(ACCEL_ADDR, reg)
		low = bus.read_byte_data(ACCEL_ADDR, reg+1)
		value = (high << 8) + low
		return value if value < 32768 else value - 65536
	x = read_word(0x3B) / 16384.0
	y = read_word(0x3D) / 16384.0
	z = read_word(0x3F) / 16384.0
	return x, y, z

# setting up the csv
CSV_FILE = "accel_data.csv"
recording = False

print("Press and hold the button to record")
timestamp = 0.0

while True:
	if button.is_pressed:
		print("Recording Started")
		with open(CSV_FILE, "w", newline="") as file:
			writer = csv.writer(file)
			writer.writerow(["TIME", "X", "Y", "Z", "COMBINED"])

		while button.is_pressed:
			x, y, z = read_accel()
			combined = math.sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2))
			timestamp = timestamp + 1.0

			with open(CSV_FILE, "a", newline="") as file:
				writer = csv.writer(file)
				writer.writerow([timestamp, x, y, z, combined])

			print(f"{timestamp} | X: {x:.4f}, Y: {y:.4f}, Z: {z:.4f}, Comb: {combined:.4f}")
			time.sleep(1)
	time.sleep(1)
	print("Not Recording")
