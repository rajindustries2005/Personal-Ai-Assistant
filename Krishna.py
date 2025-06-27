import datetime
import requests
import pyttsx3
import geocoder
import time
import socket
import os
import subprocess
import webbrowser
import smtplib
import pywhatkit
import pyautogui
import math
import cv2
import wikipedia
import wolframalpha
import imdb
from tkinter import Tk, Label, PhotoImage
from PIL import Image, ImageTk
import threading
import win32com.client as win32
import speech_recognition as sr
import pyjokes
import ctypes
import comtypes
from newsapi import NewsApiClient
import openai
import numpy as np
import pygame  # Added for sound playback
import psutil  # Added for battery status

class Krishna:
    def __init__(self):
        # Initialize pygame mixer for sound playback
        pygame.mixer.init()
        
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)  # Male voice
        self.engine.setProperty('rate', 150)  # Speaking speed
        
        # Initialize APIs with placeholder keys - replace with your actual keys
        self.newsapi = NewsApiClient(api_key='5a16e4c308ac435ab20e7ee4d8ad0858')
        self.imdb = imdb.IMDb()
        self.wolframalpha = wolframalpha.Client('Q62797-JU9GT3Y95E')
        openai.api_key = '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'
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        
        # Initialize GIF window in a separate thread
        self.gif_thread = threading.Thread(target=self._init_gif_window)
        self.gif_thread.daemon = True
        self.gif_thread.start()
        
    def _init_gif_window(self):
        """Initialize the GIF display window"""
        self.root = Tk()
        self.root.title("Krishna AI Assistant")
        self.root.geometry("1920x1080")
        
        try:
            # Load the GIF
            self.gif_path = "D:\\Personal Ai Assistant\\GIFs\\AI 2.gif"
            self.gif = PhotoImage(file=self.gif_path)
            self.gif_label = Label(self.root, image=self.gif)
            self.gif_label.pack()
            
            # For animated GIFs using PIL
            self.pil_image = Image.open(self.gif_path)
            self.frames = []
            try:
                while True:
                    self.frames.append(ImageTk.PhotoImage(self.pil_image.copy()))
                    self.pil_image.seek(len(self.frames))
            except EOFError:
                pass
            
            if len(self.frames) > 1:
                self.gif_label.destroy()
                self.animated_label = Label(self.root)
                self.animated_label.pack()
                self._animate_gif(0)
            
        except Exception as e:
            print(f"Could not load GIF: {e}")
            Label(self.root, text="Krishna AI Assistant", font=("Arial", 16)).pack()
        
        self.root.mainloop()
        
    def _animate_gif(self, frame_num):
        """Animate the GIF by cycling through frames"""
        frame = self.frames[frame_num]
        self.animated_label.configure(image=frame)
        next_frame = (frame_num + 1) % len(self.frames)
        self.root.after(100, self._animate_gif, next_frame)

        # ...existing code...
        def process_command(self, command):
            """Process user commands"""
            if not command:
                return True
    
            # Add this block for creator response
            if 'who made you' in command or 'who created you' in command or 'your creator' in command:
                self.speak("I was made by Raj Sonkar Sir.")
                return True
    # ...existing code...
            else:
                self.speak("I didn't understand that command. Can you please repeat?")
    # ...existing code...
        
    def play_startup_sound(self):
        """Play the startup sound"""
    sound_path = r"D:\Personal Ai Assistant\Sound\jarvis-147563.mp3"         

    def speak(self, text):
        """Convert text to speech"""
        print(f"Krishna: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self):
        """Listen for user commands using microphone"""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source, timeout=10)
             
        try:
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None
        except Exception as e:
            print(f"Error recognizing speech: {e}")
            return None
            
    def check_internet(self):
        """Check internet connection"""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False
            
    def get_date_time(self):
        """Get current date and time"""
        now = datetime.datetime.now()
        current_date = now.strftime("%A, %B %d, %Y")
        current_time = now.strftime("%I:%M %p")
        return current_date, current_time
        
    def get_location(self):
        """Get current location"""
        try:
            g = geocoder.ip('me')
            if g.city:
                return g.city
            return "Lucknow"
        except:
            return "Lucknow"
            
    def get_weather(self, city):
        """Get weather information for a city"""
        try:
            api_key = "2fe07c26c1735a386d3f6ab1b3043d29"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            complete_url = f"{base_url}appid={api_key}&q={city}&units=metric"
            
            response = requests.get(complete_url)
            data = response.json()
            
            if data["cod"] != "404":
                main = data["main"]
                temperature = main["temp"]
                humidity = main["humidity"]
                weather_desc = data["weather"][0]["description"]
                return temperature, humidity, weather_desc
            else:
                return None
        except:
            return None
            
    def check_rain_today(self, city):
        """Check if rain is expected today"""
        try:
            api_key = "2fe07c26c1735a386d3f6ab1b3043d29"
            base_url = "http://api.openweathermap.org/data/2.5/forecast?"
            complete_url = f"{base_url}appid={api_key}&q={city}&units=metric&cnt=8"  # 8 forecasts for 24 hours (3-hour intervals)
            
            response = requests.get(complete_url)
            data = response.json()
            
            if data["cod"] != "404":
                for forecast in data["list"]:
                    # Check if rain is in the forecast
                    if "rain" in forecast or ("weather" in forecast and any("rain" in w["description"].lower() for w in forecast["weather"])):
                        return True
                return False
            else:
                return None
        except Exception as e:
            print(f"Error checking rain forecast: {e}")
            return None
            
    def get_battery_status(self):
        """Get laptop battery status"""
        try:
            battery = psutil.sensors_battery()
            if battery is None:
                return "No battery information available"
                
            percent = battery.percent
            plugged = battery.power_plugged
            status = "plugged in" if plugged else "not plugged in"
            
            if percent <= 20 and not plugged:
                warning = "Warning: Battery is critically low! Please plug in your charger."
            elif percent <= 40 and not plugged:
                warning = "Battery is running low. Consider plugging in your charger."
            else:
                warning = ""
                
            message = f"Battery is at {percent}% and currently {status}. {warning}"
            return message.strip()
        except Exception as e:
            print(f"Error getting battery status: {e}")
            return "Could not retrieve battery information"
            
    def greet(self):
        """Greet the user based on time of day"""
        # Play startup sound
        self.play_startup_sound()
        
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            greeting = "Good morning and Jai Shree Krishna"
        elif 12 <= hour < 17:
            greeting = "Good afternoon and Jai Shree Krishna"
        else:
            greeting = "Good evening and Jai Shree Krishna"
            
        self.speak(f"{greeting}, Sir! I am Krishna.")
    
    def open_notepad(self):
        """Open Notepad"""
        try:
            subprocess.Popen(['notepad.exe'])
            self.speak("Notepad opened successfully.")
        except Exception as e:
            self.speak(f"Sorry, I couldn't open Notepad. Error: {str(e)}")
            
    def open_ms_office(self, app_name):
        """Open Microsoft Office applications"""
        try:
            if app_name.lower() == "word":
                word = win32.gencache.EnsureDispatch('Word.Application')
                word.Visible = True
                word.Documents.Add()
                self.speak("Microsoft Word opened successfully.")
            elif app_name.lower() == "excel":
                excel = win32.gencache.EnsureDispatch('Excel.Application')
                excel.Visible = True
                excel.Workbooks.Add()
                self.speak("Microsoft Excel opened successfully.")
            elif app_name.lower() == "powerpoint":
                powerpoint = win32.gencache.EnsureDispatch('PowerPoint.Application')
                powerpoint.Visible = True
                presentation = powerpoint.Presentations.Add()
                self.speak("Microsoft PowerPoint opened successfully.")
            else:
                self.speak(f"Sorry, I don't know how to open {app_name}.")
        except Exception as e:
            self.speak(f"Sorry, I couldn't open {app_name}. Error: {str(e)}")
            
    def play_on_youtube(self, query):
        """Play a video on YouTube"""
        try:
            self.speak(f"Playing {query} on YouTube")
            pywhatkit.playonyt(query)
        except Exception as e:
            self.speak(f"Sorry, I couldn't play the video. Error: {str(e)}")
            
    def shutdown_system(self, action="shutdown", delay=60):
        """Shutdown or restart the system"""
        try:
            if action.lower() == "shutdown":
                self.speak(f"System will shutdown in {delay//60} minute{'s' if delay//60 !=1 else ''}")
                os.system(f"shutdown /s /t {delay}")
            elif action.lower() == "restart":
                self.speak(f"System will restart in {delay//60} minute{'s' if delay//60 !=1 else ''}")
                os.system(f"shutdown /r /t {delay}")
            else:
                self.speak("Invalid action specified.")
        except Exception as e:
            self.speak(f"Sorry, I couldn't perform the {action}. Error: {str(e)}")
            
    def search_wikipedia(self, query):
        """Search information on Wikipedia"""
        try:
            self.speak(f"Searching Wikipedia for {query}")
            result = wikipedia.summary(query, sentences=2)
            self.speak(f"According to Wikipedia: {result}")
            return result
        except wikipedia.exceptions.DisambiguationError as e:
            self.speak(f"There are multiple options for {query}. Please be more specific.")
            return None
        except wikipedia.exceptions.PageError:
            self.speak(f"Sorry, I couldn't find any information about {query} on Wikipedia.")
            return None
        except Exception as e:
            self.speak(f"Sorry, I couldn't complete the Wikipedia search. Error: {str(e)}")
            return None
            
    def get_news(self, category='general'):
        """Get latest news from Indian sources"""
        try:
            self.speak(f"Fetching latest {category} news from India")
            news = self.newsapi.get_top_headlines(
                category=category,
                country='in',
                language='en',
                page_size=5
            )
            
            if not news['articles']:
                self.speak("No news articles found.")
                return
                
            for i, article in enumerate(news['articles'][:3], 1):
                title = article.get('title', 'No title')
                source = article.get('source', {}).get('name', 'Unknown source')
                self.speak(f"News {i} from {source}: {title}")
                time.sleep(1)
                
            self.speak("That's the latest news update.")
            
        except Exception as e:
            self.speak(f"Sorry, I couldn't fetch the news. Error: {str(e)}")
            
    def calculate_math(self, expression):
        """Perform mathematical calculations"""
        try:
            self.speak(f"Calculating {expression}")
            res = self.wolframalpha.query(expression)
            answer = next(res.results).text
            self.speak(f"The answer is {answer}")
            return answer
        except Exception as e:
            try:
                # Fallback to eval for simple calculations
                result = eval(expression)
                self.speak(f"The answer is {result}")
                return result
            except:
                self.speak(f"Sorry, I couldn't calculate that. Error: {str(e)}")
                return None
                
    def ask_chatgpt(self, question):
        """Get information using ChatGPT with enhanced capabilities"""
        try:
            self.speak(f"Let me think about: {question}")
            
            # Use the latest GPT-4 model if available, otherwise fall back to GPT-3.5
            model = "gpt-4" if "gpt-4" in [m.id for m in openai.Model.list()["data"]] else "gpt-3.5-turbo"
            
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are Krishna, a highly intelligent AI assistant. Provide detailed, accurate responses."},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            answer = response.choices[0].message.content
            self.speak(f"Here's what I found: {answer}")
            return answer
        except Exception as e:
            self.speak(f"Sorry, I couldn't get an answer from ChatGPT. Error: {str(e)}")
            return None
            
    def get_movie_details(self, movie_name):
        """Get movie details from IMDb"""
        try:
            self.speak(f"Searching for {movie_name} on IMDb")
            movies = self.imdb.search_movie(movie_name)
            if not movies:
                self.speak("No movie found with that name.")
                return
            
            movie_id = movies[0].getID()
            movie = self.imdb.get_movie(movie_id)
            
            title = movie.get('title', 'N/A')
            year = movie.get('year', 'N/A')
            rating = movie.get('rating', 'N/A')
            directors = ', '.join([d['name'] for d in movie.get('directors', [])]) or 'N/A'
            cast = ', '.join([c['name'] for c in movie.get('cast', [])[:5]]) or 'N/A'
            plot = movie.get('plot outline', 'N/A')
            
            response = (
                f"Here's what I found about {title}:\n"
                f"Year: {year}\n"
                f"IMDb Rating: {rating}\n"
                f"Directed by: {directors}\n"
                f"Cast includes: {cast}\n"
                f"Plot: {plot}"
            )
            
            print(response)
            self.speak(f"I found information about {title}. It was released in {year} with an IMDb rating of {rating}.")
            self.speak(f"It was directed by {directors} and features actors like {cast}.")
            self.speak(f"Here's a brief plot: {plot}")
            
        except Exception as e:
            self.speak(f"Sorry, I couldn't fetch movie details. Error: {str(e)}")
            
    def tell_joke(self):
        """Tell a random joke"""
        try:
            joke = pyjokes.get_joke()
            self.speak(joke)
        except Exception as e:
            self.speak(f"Sorry, I couldn't think of a joke right now. Error: {str(e)}")
            
    def open_website(self, url):
        """Open a website in default browser"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            webbrowser.open(url)
            self.speak(f"Opening {url}")
        except Exception as e:
            self.speak(f"Sorry, I couldn't open that website. Error: {str(e)}")

    def process_command(self, command):
        """Process user commands"""
        if not command:
            return True
            
        # Basic commands
        if 'time' in command:
            _, time_now = self.get_date_time()
            self.speak(f"The current time is {time_now}")
            
        elif 'date' in command:
            date, _ = self.get_date_time()
            self.speak(f"Today is {date}")
            
        elif 'weather' in command:
            city = self.get_location()
            weather_data = self.get_weather(city)
            if weather_data:
                temp, humidity, desc = weather_data
                self.speak(f"The current weather in {city} is {desc}")
                self.speak(f"Temperature is {temp}°C with humidity at {humidity}%")
                
                # Check if rain is expected today
                if 'rain' in command or 'will it rain' in command:
                    rain_expected = self.check_rain_today(city)
                    if rain_expected is True:
                        self.speak("Yes, rain is expected today. You might want to carry an umbrella.")
                    elif rain_expected is False:
                        self.speak("No rain is expected today. Enjoy the weather!")
                    else:
                        self.speak("I couldn't check the rain forecast right now.")
            else:
                self.speak("Sorry, I couldn't fetch the weather information")
                
        # Battery status
        elif 'battery' in command or 'power' in command:
            battery_status = self.get_battery_status()
            self.speak(battery_status)
                
        # Application controls
        elif 'open notepad' in command:
            self.open_notepad()
            
        elif 'open word' in command:
            self.open_ms_office('word')
            
        elif 'open excel' in command:
            self.open_ms_office('excel')
            
        elif 'open powerpoint' in command:
            self.open_ms_office('powerpoint')
            
        # Media controls
        elif 'play' in command and 'youtube' in command:
            query = command.replace('play', '').replace('on youtube', '').strip()
            if query:
                self.play_on_youtube(query)
                
        # System controls
        elif 'shutdown' in command:
            self.shutdown_system('shutdown')
            
        elif 'restart' in command:
            self.shutdown_system('restart')
            
        # Information queries
        elif 'who is' in command or 'what is' in command:
            query = command.replace('who is', '').replace('what is', '').strip()
            self.search_wikipedia(query)
            
        elif 'news' in command:
            category = 'general'
            if 'sports' in command:
                category = 'sports'
            elif 'technology' in command:
                category = 'technology'
            self.get_news(category)
            
        # Math calculations
        elif 'calculate' in command:
            expression = command.replace('calculate', '').strip()
            self.calculate_math(expression)
            
        # ChatGPT integration
        elif 'ask' in command or 'tell me' in command or 'explain' in command:
            question = command.replace('ask', '').replace('tell me', '').replace('explain', '').strip()
            self.ask_chatgpt(question)
            
        # Movies
        elif 'movie' in command and ('about' in command or 'details' in command):
            movie_name = command.replace('movie', '').replace('about', '').replace('details', '').strip()
            self.get_movie_details(movie_name)
            
        # Jokes
        elif 'joke' in command or 'funny' in command:
            self.tell_joke()
            
        # Open website
        elif 'open website' in command or 'open' in command:
            url = command.replace('open website', '').replace('open', '').strip()
            self.open_website(url)
                
        # Exit command
        elif 'exit' in command or 'goodbye' in command or 'quit' in command:
            self.speak("Radhe Radhe Sir.")
            return False
            
        else:
            self.speak("I didn't understand that command. Can you please repeat?")
            
        return True

    def run(self):
        """Main execution loop for Krishna"""
        # Check internet connection
        if not self.check_internet():
            self.speak("Sir, your WiFi is off. Please connect to the internet to use my services.")
            return
            
        # Initial greeting and information
        self.greet()
        time.sleep(1)
        
        date, time_now = self.get_date_time()
        self.speak(f"Today is {date}")
        self.speak(f"The current time is {time_now}")
        time.sleep(1)
        
        city = self.get_location()
        weather_data = self.get_weather(city)
        if weather_data:
            temp, humidity, desc = weather_data
            self.speak(f"The current weather in {city} is {desc}")
            self.speak(f"Temperature is {temp}°C with humidity at {humidity}%")
            
            # Check if rain is expected today during startup
            rain_expected = self.check_rain_today(city)
            if rain_expected is True:            # ...existing code...
                def process_command(self, command):
                    """Process user commands"""
                    if not command:
                        return True
            
                    # Add this block for creator response
                    if 'who made you' in command or 'who created you' in command or 'your creator' in command:
                        self.speak("I was made by Raj Sonkar Sir.")
                        return True
            # ...existing code...
                    else:
                        self.speak("I didn't understand that command. Can you please repeat?")
            # ...existing code...
                self.speak("By the way, rain is expected today. You might want to carry an umbrella.")
            elif rain_expected is False:
                self.speak("No rain is expected today. Enjoy the weather!")
        else:
            self.speak("I couldn't retrieve the weather information right now")
        
        # Check battery status during startup
        battery_status = self.get_battery_status()
        self.speak(battery_status)
        
        # Main command loop
        running = True
        while running:
            self.speak("How may I assist you?")
            command = self.listen()
            if command:
                running = self.process_command(command)
            else:
                self.speak("I didn't catch that. Could you please repeat?")
            time.sleep(1)

if __name__ == "__main__":
    print("Initializing Krishna...")
    Krishna = Krishna()
    Krishna.run()
