import serial
import time
import csv
import matplotlib.pyplot as plt

BUFFER_SIZE = 64  # Must match the Metro's buffer size
OUTPUT_FILE = "drop_data.csv"

# Initialize UART (adjust port if needed)
ser = serial.Serial('/dev/serial0', 115200, timeout=1)

def receive_csv():
    """ Receives a CSV file over UART and saves it locally. """
    with open(OUTPUT_FILE, "wb") as f:
        while True:
            data = ser.read(BUFFER_SIZE)  # Read chunk from UART
            if not data:
                time.sleep(0.01)  # No data received, wait and retry
                continue

            # Check for EOF marker
            if b"EOF" in data:
                data = data.replace(b"EOF", b"")  # Remove EOF marker
                f.write(data)
                break

            f.write(data)  # Write chunk to file
            ser.flush()  # Ensure data is sent immediately

    print("CSV transfer complete!")

def plot_acceleration():
    """ Reads the CSV file, plots acceleration vs. time, and prints the surface type. """
    timestamps = []
    acceleration = []
    surface_type = None  # To store the surface type from the last row

    try:
        with open(OUTPUT_FILE, mode="r") as file:
            reader = csv.reader(file)
            header = next(reader, None)  # Skip header row

            for row in reader:
                if len(row) < 2:
                    continue  # Skip incomplete rows

                try:
                    timestamps.append(float(row[0]))  # Time (ms)
                    acceleration.append(float(row[1]))  # Acceleration (m/sÂ²)
                except ValueError:
                    continue  # Skip bad rows

                # Capture the last row's surface type (column index 4)
                if len(row) >= 5:  # Ensure column exists
                    surface_type = row[4]  # Get last surface type entry

        if not timestamps or not acceleration:
            print("Error: No valid data found in CSV.")
            return

        # Print the surface type (if found)
        if surface_type:
            print(f"Surface Type: {surface_type}")

        # Plot acceleration vs time
        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, acceleration, label="Acceleration", color="blue", linestyle="-")

        plt.xlabel("Time (ms)")
        plt.ylabel("Acceleration (m/sÂ²)")
        plt.title(f"Acceleration vs. Time ({surface_type})")  # Show surface type in title
        plt.legend()
        plt.grid(True)

        # Save and display the plot
        plt.savefig("acceleration_plot.png")
        plt.show()

    except Exception as e:
        print(f"Error reading or plotting CSV: {e}")

if __name__ == "__main__":
    time.sleep(1)  # Wait 1 second
    receive_csv()
    ser.close()

    # Plot the acceleration values and print surface type
    plot_acceleration()

