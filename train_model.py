import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("labeled_data.csv")

input_cols = ['Avg Accel', 'Standard Deviation', 'Peak Accel', 'Accel Range', 'Num of Peaks']
output_col = 'Surface Type'

# Extract features and labels
X = df[input_cols].values  # Only using acceleration for now
y = df[output_col].values  # Classification labels (0 = Soft, 1 = Hard)

# Normalize features
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Train-test split
train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.2, random_state=42)

# Define a simple neural network model
model = keras.Sequential([
    keras.layers.Dense(8, activation='relu', input_shape=(1,)),
    keras.layers.Dense(4, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

# Compile and train the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(train_X, train_y, epochs=50, batch_size=4, validation_data=(test_X, test_y))

# Save model
model.save("surface_classifier.h5")
print("Model saved as surface_classifier.h5")
