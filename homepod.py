import openai
import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup
import subprocess

openai.api_key = 'your_openai_api_key_here'

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

tts_engine.setProperty('rate', 150)
tts_engine.setProperty('volume', 1.0)

def play_sound(filename):
    """Play a sound file."""
    subprocess.run(['mpg123', filename])

def listen():
    """Listen for voice input."""
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f"Recognized: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError as e:
            speak(f"Sorry, I'm having trouble connecting to the service. Error: {e}")
            return None

def speak(text):
    """Convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def search_web(query):
    """Perform a web search and return a summary of the first result."""
    google_api_key = 'your_google_api_key_here'
    search_engine_id = 'your_search_engine_id_here'
    search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={google_api_key}&cx={search_engine_id}"
    
    response = requests.get(search_url)
    search_results = response.json()
    
    if search_results.get('items'):
        first_result = search_results['items'][0]
        title = first_result['title']
        snippet = first_result['snippet']
        link = first_result['link']
        result_summary = f"Here's what I found: {title}. {snippet}. You can read more here: {link}"
        return result_summary
    else:
        return "Sorry, I couldn't find any information on that."

def chat_with_gpt(prompt):
    """Send the prompt to OpenAI API and get the response."""
    response = openai.Completion.create(
        engine="gpt-4",  
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def main():
    """Main loop for the virtual assistant."""
    while True:
        user_input = listen()
        if user_input:
            if any(phrase in user_input.lower() for phrase in ["goodbye", "exit", "quit", "stop"]):
                speak("Goodbye! Have a great day!")
                break
            else:
                if any(phrase in user_input.lower() for phrase in ["search", "find", "look up", "what is", "who is"]):
                    result = search_web(user_input)
                    speak(result)
                else:
                    response = chat_with_gpt(user_input)
                    speak(response)

if __name__ == "__main__":
    main()
