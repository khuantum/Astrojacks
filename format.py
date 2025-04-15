from micromlgen import port

# Load the TFLite model
with open("surface_classifier.tflite", "rb") as f:
    tflite_model = f.read()

# Convert to C header file format
c_model = port(tflite_model)

# Save as a C header file
with open("model_data.h", "w") as f:
    f.write(c_model)

print("TensorFlow Lite model converted to C header file: model_data.h") 
