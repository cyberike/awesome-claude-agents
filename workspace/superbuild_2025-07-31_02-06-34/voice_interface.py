import speech_recognition as sr
import pyttsx3

class VoiceInterface:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand.")
        except sr.RequestError as e:
            print(f"Could not request results: {e}")

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    interface = VoiceInterface()
    while True:
        text = interface.listen()
        if text:
            if "hello" in text.lower():
                interface.speak("Hello! How can I assist you?")
            elif "goodbye" in text.lower():
                interface.speak("Goodbye!")
                break
            else:
                interface.speak("You said: " + text)
