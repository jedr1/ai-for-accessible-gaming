import pyttsx3
import speech_recognition as sr

def speak(text):
  speech_engine = pyttsx3.init() # Initialise the speech synthesis engine
  speech_engine.say(text) # Queue the text to be spoken
  speech_engine.runAndWait() # Run engine, speak queued up text, block program until speech is finished

def listen():
  recongiser = sr.Recognizer() # Create Recognizer object
  # Open your systems microphone and assign it to the source variable
  with sr.Microphone() as source: 
    print("Listening...")
    # Record audio from microphone, store captured audio in the audio variable
    audio = recongiser.listen(source) 
  
  try: # Start try block, which catches errors that may occur in this block
    # Use offline speech recognition engine (CMU Spjinx) to transcribe audio into text
    response = recongiser.recognize_sphinx(audio)
    print(f"You said: {response}")
    return response.lower() #Return transcribed text in lowercase
  except sr.UnknownValueError:
        print("Sorry, I did not catch that.")
        return ""
  except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""

def ask_question(question):
   speak(question)
   answer = listen().lower().strip()

   if any(yes_word in answer for yes_word in ['yes', 'yeah', 'yup', 'sure', 'please do']):
      print('User said yes')
      return True
   elif any(no_word in answer for no_word in ['no', 'nope', 'nah']):
      print("User said no")
      return False
   else:
      print("I didn't understand your response")