from .constants import class_names
from keras.src.legacy.preprocessing.image import ImageDataGenerator
import os

temp_directory = "temp"

# Resize and split data into training and validation (This should be the same as values used last time)
image_size = (160, 160)
image_data_generator = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
)

# A function used to know when the program should fine tune the model, or collect more data
def validate_temp_data(min_number_of_images):
    class_folder_count = 0
    total_images = 0

    for class_name in class_names.values():
        class_directory = os.path.join(temp_directory, class_name)

        if os.path.exists(class_directory):
            class_folder_count += 1
            num_images_in_class = len([file for file in os.listdir(class_directory)]) 
            total_images += num_images_in_class
    
    return class_folder_count == len(class_names) and total_images >= min_number_of_images

def fine_tune_model(model):
    print("Fine tuning model...")

    new_data_generator = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )

    new_training_data = new_data_generator.flow_from_directory(
        temp_directory,
        target_size=image_size,
        batch_size=2,
        class_mode='categorical',
        subset='training'
    )

    new_validation_data = new_data_generator.flow_from_directory(
        temp_directory,
        target_size=image_size,
        batch_size=2,
        class_mode='categorical',
        subset='validation'
    )
    
    history = model.fit(
        new_training_data,
        validation_data=new_validation_data, 
        epochs=5,
        verbose=1
    )

    print('Saving model...')
    model.save("models/updated_low_vision_classifier.keras")
    print('Model saved at: models/updated_low_vision_classifier.keras')