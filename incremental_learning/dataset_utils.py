from datetime import datetime
import os

def save_new_data(low_vision_class, pil_image):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/{low_vision_class}/{timestamp}.png"
    # Save image to the dataset with the user specified label
    pil_image.save(filename)
    print(f"Screenshot saved to {filename}")

    temp_folder_path = f"temp_data/{low_vision_class}"
    # If folder path doesn't exist, create it
    os.makedirs(temp_folder_path, exist_ok=True)
    temp_filename = f"{temp_folder_path}/{timestamp}.png"
    # Save to temporary dataset
    pil_image.save(temp_filename)
    print(f"Screenshot saved to {temp_filename}")