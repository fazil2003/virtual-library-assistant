import sys
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import resnet50

# Load the Keras image database
model = resnet50.ResNet50()

# Load the picture as 224x224 (maximum size this model can cope with)
picture = image.load_img(r"/media/mohamedfazil/Projects/Final Year Project/library/python_files/flask_image_search/static/img/comp1.jpg", target_size=(224, 224))

# Convert to image array
x = image.img_to_array(picture)

# Expand as if it is an array of images
x = np.expand_dims(x, axis=0)

# Pre-process to the scale of the trained network
x = resnet50.preprocess_input(x)

# Run the prediction
predictions = model.predict(x)

# Get the classes of the top 10 results
predicted_classes = resnet50.decode_predictions(predictions, top=10)

print("YOUR PICTURE IS OF A:")

for imagenet_id, name, likelihood in predicted_classes[0]:
    print(" - {}: {}".format(name, likelihood))

