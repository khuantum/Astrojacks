import serial
import pandas as pd
import time






# =================================================================
# !!!                        README                             !!!
# =================================================================
# This file is used to run a data logging program on the RasPi






# Adjust the serial port (COMx for Windows, /dev/ttyUSBx for Linux/Mac)
SERIAL_PORT = 'COMx'  # TODO: Check Device Manager -> Ports -> Active ports. Change this field to the controller (RasPi or Metro M4) port
BAUD_RATE = 115200
DURATION = 60  # Collect data for 60 seconds

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
log_data = []

start_time = time.time()
print("Collecting data...")

try:
    while time.time() - start_time < DURATION:
        line = ser.readline().decode().strip()
        if line:
            values = line.split(',')
            if len(values) == 3:  # Assuming X, Y, Z acceleration
                timestamp = time.time()
                log_data.append([timestamp] + list(map(float, values)))

    df = pd.DataFrame(log_data, columns=['Timestamp (ms)', 'Total Accel (m/s^2)', 'Peak Drop Acceleration (m/s^2)', 'Impact Duration (ms)'])
    df.to_csv('drop_data.csv', index=False)
    print("Data saved to drop_data.csv. Check directory.")

except KeyboardInterrupt:
    ser.close()
