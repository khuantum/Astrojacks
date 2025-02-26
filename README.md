# Astrojacks
Aaron's Branch

For ML files:

- data_logging.py: Data logger using accelerometer. Saves to CSV file
- data_processor.py: Data processor. Returns new CSV file
- train_surface_classifier.py: Model trainer for classifying surface hardness
- model_converter.py: Program for converting PyTorch model into TFLite, which will then be converted to TinyML. 

Procedure:
1. Run data_logging.py to get raw .csv
2. Run data_processor.py
3. Run train_surface_classifier.py. Should see surface_classifier.pth in directory.
4. Run model_converter.py. Should see surface_classifier.onnx in directory




WELCOME
