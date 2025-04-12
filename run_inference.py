import pandas as pd
import tensorflow.lite as tflite
import numpy as np

# Load the CSV file
df = pd.read_csv("input_data.csv")

# Load the TensorFlow Lite model
interpreter = tflite.Interpreter(model_path="surface_classifier.tflite")
interpreter.allocate_tensors()

# Get input and output tensor details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Extract acceleration values from the CSV
X_input = df["Acceleration"].values.reshape(-1, 1)  # Reshape for model input

# Run predictions on each row
predictions = []

for value in X_input:
    # Reshape input to match model's expected shape
    input_data = np.array([value], dtype=np.float32).reshape(1, 1)
    
    # Set input tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)
    
    # Run inference
    interpreter.invoke()
    
    # Get output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    # Interpret the result
    prediction = "Hard" if output_data[0][0] > 0.5 else "Soft"
    predictions.append(prediction)

# Append predictions to CSV
df["Prediction"] = predictions
df.to_csv("output_predictions.csv", index=False)

print("   Inference completed. Predictions saved in output_predictions.csv   ")
