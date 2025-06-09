import sys
import os

# Add the parent directory to the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from speech_utils.speech_utils import ask_question
from accessibility_settings.accessibility_settings_utils import write_settings
from incremental_learning.dataset_utils import save_new_data

def handleLowVision(low_vision_type, screenshot):
  match low_vision_type:
    case 'low_vision_dark':
      answer = ask_question('Shall I increase brightness?')
      if answer is True:
        write_settings('brightness_mode', 'on')
        save_new_data('low_vision_dark', screenshot)
      elif answer is False:
        write_settings('brightness_mode', 'off')
      
    case 'low_vision_cluttered':
      answer = ask_question('Shall I zoom out?')
      if answer is True:
        write_settings('zoom_out', 'on')
        save_new_data('low_vision_cluttered', screenshot)
      elif answer is False:
        write_settings('zoom_out', 'off')