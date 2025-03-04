import serial
import time

BUFFER_SIZE = 64  # Must match the Metro's buffer size
OUTPUT_FILE = "test3.csv"

# Initialize UART (adjust port if needed)
ser = serial.Serial('/dev/serial0', 115200, timeout=1)

def receive_csv():
    with open(OUTPUT_FILE, "wb") as f:
        while True:
            data = ser.read(BUFFER_SIZE)  # Read chunk from UART
            if not data:
                # No data received; wait a little and try again
                time.sleep(0.01)
                continue

            # Check if the received data contains the EOF marker
            if b"EOF" in data:
                # Remove the EOF marker before writing (if any)
                data = data.replace(b"EOF", b"")
                f.write(data)
                break
            
            f.write(data)  # Write chunk to CSV file
            ser.flush()      # Ensure the data is sent immediately

    print("CSV transfer complete!")

if __name__ == "__main__":
    time.sleep(1) #wait 1 second
    receive_csv()
    ser.close()
    

