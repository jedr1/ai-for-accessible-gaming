from incremental_learning.fine_tune_model_utils import fine_tune_model, validate_temp_data
from incremental_learning.constants import class_indexes, class_names
from actions.actions_utils import handleLowVision
import numpy as np
import mss
import time
from keras._tf_keras.keras.models import load_model
from keras.src.legacy.preprocessing.image import ImageDataGenerator
import shutil
from PIL import Image

print("Loading model...")
# The arguement here should reference the model we trained in the last module
model = load_model("models/updated_low_vision_classifier.keras")
print("Model loaded")

# Resize and split data into training and validation (This should be the same as values used last time)
image_size = (160, 160)
image_data_generator = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
)

# Freeze all layers in the neural network except the last two, these are the ones we want to fine tune
for layer in model.layers[:-2]:
    layer.trainable = False

# A temporary directory new, labelled screenshots will get saved to before the model is fine-tuned
temp_directory = "temp_data"

# Initialise the screenshot tool
screen_capture_tool = mss.mss()
primary_screen = screen_capture_tool.monitors[0]

# Start a continuous loop
while True:
    if (validate_temp_data(34)):
        fine_tune_model()
        # Remove the temp_data directory once the model has been fine tuned with the images inside it
        shutil.rmtree("temp_data")

    # Run the loop every 5 seconds
    time.sleep(5)

    # Take the screenshot
    screenshot = screen_capture_tool.grab(primary_screen)
    
    # Convert to PIL Image if needed
    if not isinstance(screenshot, Image.Image):
        screenshot = Image.fromarray(np.asarray(screenshot))

    # Convert image to a NumPy array with the shape expected by the model (0, 160, 160, 3)
    screenshot = screenshot.convert("RGB")
    screenshot = screenshot.resize(image_size)
    image_array = np.asarray(screenshot).astype(np.float32) # Convert the screenshot to a NumPy array with float32 dtype

    # Pre process the screenshot so its ready to be passed into our model
    image = image_data_generator.standardize(image_array)

    # Add batch dimension
    image = np.expand_dims(image, axis=0)

    # Make a prediction based on this screenshot
    predictions = model.predict(image)
    
    # Get the predicted class with the highest probability
    predicted_class = np.argmax(predictions, axis=1)[0]

    print(f"Predicted class: {class_names[predicted_class]}")

    if predicted_class != class_indexes['non_low_vision']: 
        handleLowVision(class_names[predicted_class], screenshot)
    else:
      print("non_low_vision detected")