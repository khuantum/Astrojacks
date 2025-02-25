import pandas as pd
import numpy as np

# Load raw data
df = pd.read_csv("data.csv")

# Compute features
df['Magnitude'] = np.sqrt(df['Accel_X']**2 + df['Accel_Y']**2 + df['Accel_Z']**2)

# Extract peak acceleration
peak_accel = df['Magnitude'].max()

# Compute mean acceleration over time window
mean_accel = df['Magnitude'].mean()

# Compute impact duration (approx.)
impact_duration = df[df['Magnitude'] > 0.5]['Timestamp'].max() - df['Timestamp'].min()

# Label manually (1 = Hard Surface, 0 = Soft Surface)
# Change label manually for each dataset you collect
label = 1  # Change this for each dataset collected

# Save processed data
processed_df = pd.DataFrame([[peak_accel, mean_accel, impact_duration, label]],
                            columns=['Peak_Accel', 'Mean_Accel', 'Impact_Duration', 'Label'])

processed_df.to_csv("processed_surface_data.csv", index=False)
print("Processed data saved to processed_surface_data.csv")
