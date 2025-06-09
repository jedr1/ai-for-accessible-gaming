import os

SETTINGS_FILENAME = "minecraft-accessibility-settings.txt"
SETTINGS_PATH = os.path.join(os.path.expanduser("~"), SETTINGS_FILENAME)

def read_settings():
    settings = {} # Initialise settings dictionary
    if os.path.exists(SETTINGS_PATH): # If it finds the settings file
        with open(SETTINGS_PATH, "r") as file: # Open the settings file in read mode
            for line in file: # For each line
                if "=" in line:
                    key, value = line.strip().split("=", 1) # Extract the key and value from each pair
                    settings[key.strip().lower()] = value.strip().lower() # Append the settings dictionary with the key/value pair
    return settings # return the settings as a dictionary

def write_settings(key, value):
    settings = read_settings() # Fetch the current settings and store the dictionary in settings
    settings[key.lower()] = value.lower() # Change the specified key's value to the given value arguement

    # Open the file in write mode and rewrite the file with the new changes
    with open(SETTINGS_PATH, "w") as file:
        for k, v in settings.items():
            file.write(f"{k}={v}\n")