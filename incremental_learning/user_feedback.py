import tkinter as tk
from PIL import ImageTk
from datetime import datetime
from constants import class_names
import os

class LowVisionFeedback:
      # Set instance variables on initialisation of the object
      def __init__(self, predicted_class, screenshot):
          self.predicted_class = predicted_class
          self.pil_image = screenshot.resize((400, 300))
          self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

      def ask_for_feedback(self):
           self.create_feedback_window()

      # Reusable function to create a pop up window 
      def show_input_modal(self, title, prompt_text, on_submit, with_image=False):
          # Create a new top-level window using the tkinter library
          window = tk.Tk()
          # Set the title of the window
          window.title(title) 

          if with_image:
              # Convert the PIL image into a format compatible with tkinter
              tk_image = ImageTk.PhotoImage(self.pil_image)
              # Create a label widget to hold the image
              label_img = tk.Label(window, image=tk_image)
              # Keep a reference to the image to prevent it from being garbage collected
              label_img.image = tk_image
              # Add the image label to the window
              label_img.pack()
          
          # Create and add a text label to prompt the user
          label = tk.Label(window, text=prompt_text)
          # Add padding to the label
          label.pack(pady=10)

          # Create and add an entry widget where the user can type input
          entry = tk.Entry(window, font=("Arial", 14))
          entry.pack(pady=10)

          # Method that gets called when the submit button is clicked
          def submit():
              # Get the user's input, strip whitespace, and convert to lowercase
              response = entry.get().strip().lower()
              # Quit the tkinter mainloop
              window.quit()
              # Destroy the window
              window.destroy()
              # Call the provided callback function with the user's input
              on_submit(response)

          # Create and add a button that triggers the submit function
          submit_button = tk.Button(window, text="Submit", command=submit)
          submit_button.pack()

          # Start the tkinter event loop to display the window and wait for interaction
          window.mainloop()
      
      def create_feedback_window(self):
           self.show_input_modal(
                title=f"User Feedback - Potential {class_names[self.predicted_class]}",
                prompt_text="Is this a low vision scene? (Y/N)",
                on_submit=self.process_first_response, # Function to get called when the submit button is clicked
                with_image=True
           )
           
      def process_first_response(self, response):
           if response in ["y", "yes"]:
                self.ask_for_low_vision_type()
           else:
                self.ask_if_valid_non_vision()
      
      def ask_for_low_vision_type(self):
           self.show_input_modal(
                title="Low Vision Type",
                prompt_text="What type of low vision scene is this? (Dark / Bright / Cluttered)",
                on_submit=self.process_low_vision_type
           )  

      def process_low_vision_type(self, user_input):
           if (user_input is None):
                print("User did not specify a low vision type")
                return

           folder_name = self.get_low_vision_type_from_input(user_input)
           if folder_name:
                filename = f"data/{folder_name}/{user_input.lower()}_{self.timestamp}.png"
                # Save image to the dataset with the user specified label
                self.pil_image.save(filename)
                print(f"Screenshot saved to {filename}")

                temp_folder_path = f"temp_data/{folder_name}"
                # If folder path doesn't exist, create it
                os.makedirs(temp_folder_path, exist_ok=True)
                temp_filename = f"{temp_folder_path}/{user_input.lower()}_{self.timestamp}.png"
                # Save to temporary dataset
                self.pil_image.save(temp_filename)
                print(f"Screenshot saved to {temp_filename}")
               
           else:
                print("Invalid low vision type. Screenshot not saved.")


      def get_low_vision_type_from_input(self, second_response):
        if second_response == "dark":
            return "low_vision_dark"
        elif second_response == "bright":
            return "low_vision_bright"
        elif second_response == "cluttered":
            return "low_vision_cluttered"
        else:
            return None 
        

      def ask_if_valid_non_vision(self):
           self.show_input_modal(
               title="Valid Non Low Vision",
               prompt_text="Is this a valid non low vision?",
               on_submit=self.process_non_low_vision_screenshot
           )

      def process_non_low_vision_screenshot(self, user_input):
          if user_input in ["y", "yes"]:
              self.save_non_low_vision_screenshot()
          else:
              print("Invalid screenshot. Not saved.")

      def save_non_low_vision_screenshot(self):
        filename = f"data/non_low_vision/{self.timestamp}.png"
        self.pil_image.save(filename)
        print(f"Screenshot saved to {filename}")

        temp_folder_path = "temp_data/non_low_vision"
        temp_filename = f"{temp_folder_path}/{self.timestamp}.png"
        os.makedirs(temp_folder_path, exist_ok=True)

        self.pil_image.save(temp_filename)
        print(f"Screenshot saved to {temp_filename}")


def ask_user_for_feedback(predicted_class, screenshot):
     # Create an instance of the LowVisionFeedback class, passing in the prediction and screenshot
     feedback = LowVisionFeedback(predicted_class, screenshot)
     # Call the method that handles displaying the feedback prompt to the user
     feedback.ask_for_feedback()