import torch
import onnx
import train_surface_classifier as tsc







# !!!                        IMPORTANT                          !!!
# =================================================================
# This is the file for converting the PyTorch model into a TensorFlow model
# Please run train_surface_classifier.py before running this one
# =================================================================







# Define the model structure again
model = tsc.SurfaceClassifier()
model.load_state_dict(torch.load("surface_classifier.pth"))
model.eval()

# Dummy input tensor (3 features: Peak_Accel, Mean_Accel, Impact_Duration)
dummy_input = torch.randn(1, 3)

# Convert to ONNX
onnx_file = "surface_classifier.onnx"
torch.onnx.export(model, dummy_input, onnx_file, input_names=["input"], output_names=["output"])
print(f"Model converted to {onnx_file}")
