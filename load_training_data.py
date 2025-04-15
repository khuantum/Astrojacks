import pandas as pd
import glob
from scipy.signal import find_peaks

# List to store the result
data = []

# Get all CSV files (adjust pattern as needed)
soft_csv_files = glob.glob("soft_surface_sample_*.csv") 
hard_csv_files = glob.glob("hard_surface_sample_*.csv")

csv_files = soft_csv_files.append(hard_csv_files)

for file in csv_files:
    df = pd.read_csv(file)
    accel_data = df["Total Accel (m/s^2)"]

    # Make sure required columns exist
    if "Total Accel (m/s^2)" in df.columns and "Surface Type" in df.columns:
        avg_accel = accel_data.mean()
        std_dev = accel_data.std()
        max_accel = accel_data.max()
        range = max_accel - accel_data.min()

        peaks, _ = find_peaks(accel_data)
        num_peaks = len(peaks)

        surface_type_str = df["Surface Type"].iloc[0].strip().lower()

        # Map surface type to binary label
        if surface_type_str == "soft":
            label = 0
        elif surface_type_str == "hard":
            label = 1
        else:
            print(f"Unknown surface type in {file}. Skipping.")
            continue

        data.append({
            "Avg Accel": avg_accel,
            "Standard Deviation": std_dev,
            "Peak Accel": max_accel,
            "Accel Range": range,
            "Num of Peaks": num_peaks,
            "Surface Type": label
        })

# Create the final DataFrame and save it
result_df = pd.DataFrame(data)
result_df.to_csv("labeled_data.csv", index=False)
print("Saved to labeled_data.csv")