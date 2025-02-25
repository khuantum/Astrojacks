import csv
import matplotlib.pyplot as plt

# File name
filename = input("Enter exact csv file name: ")

# Lists to store data
time = []
x_accel = []
y_accel = []
z_accel = []
comb_accel = []

# Read the CSV file
with open(filename, mode="r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    for row in reader:
        time.append(float(row[0]))
        x_accel.append(float(row[1]))
        y_accel.append(float(row[2]))
        z_accel.append(float(row[3]))
        comb_accel.append(float(row[4]))

# Create the plot
plt.figure(figsize=(10, 5))
plt.plot(time, x_accel, label="X Acceleration", color="r", linestyle="-.")
plt.plot(time, y_accel, label="Y Acceleration", color="g", linestyle="--")
plt.plot(time, z_accel, label="Z Acceleration", color="b", linestyle=":")
plt.plot(time, comb_accel, label = "Combined Acceleration", color="black", linestyle="-")
# Formatting
plt.xlabel("Time (s)")
plt.ylabel("Acceleration")
plt.title("Acceleration vs. Time")
plt.legend()
plt.grid(True)

# Show the graph
plt.savefig("sample_plot.png")
