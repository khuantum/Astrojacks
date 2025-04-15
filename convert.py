import tensorflow as tf

# Load trained model
model = tf.keras.models.load_model("surface_classifier.h5")

# Convert model to TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # Optimize for TinyML
converter.target_spec.supported_types = [tf.float16]  # Reduce model size
tflite_model = converter.convert()

# Save the TensorFlow Lite model
with open("surface_classifier.tflite", "wb") as f:
    f.write(tflite_model)

print("TensorFlow model converted to TensorFlow Lite: surface_classifier.tflite")