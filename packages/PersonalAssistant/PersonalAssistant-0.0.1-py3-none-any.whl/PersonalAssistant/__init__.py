import datetime
import pyttsx3
import pyjokes
import smtplib
import webbrowser as web
import speech_recognition as sr
import requests
import sys
import wikipedia
from email.mime.multipart import MIMEMultipart
import pafy
import random

__author__ = "Debadrito Dutta (dipalidutta312@gmail.com)"
__version__ = "0.0.1"

class Assistant:
    def __init__(self, name: str, voice: int, news_api_key: str, your_google_pass : str, your_google_email : str):
        """
        Creates a new Voice assistant instance.

        Parameters
        ----------
            name : str
                name of the assistant
            voice : int
                voice id of the assistant
            news_api_key : str
                the api key for fetching the news from the news api
            your_google_pass : str
                Your google account password to send emails
            your_google_email : str
                Your google account email to send and recieve emails
        """
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 160)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[voice].id)
        self.working = True
        self.name = name
        self.news_api_key = news_api_key
        self.password = your_google_pass
        self.email = your_google_email

    def speak(self, audio):
        """
        String representation of parameter "audio" will be converted to speech using self.engine

        :param audio: str
        :return: None
        """
        print(": {}".format(audio))
        self.engine.say(audio)
        self.engine.runAndWait()
    def Speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def WishMe(self):
        """
        Personal assistant will greet you with the appropriate greeting depending on the current time

        :return: None
        """
        hour = int(datetime.datetime.now().hour)
        if hour >= 5 and hour < 12:
            self.speak('Good Morning')
        elif hour >= 12 and hour<17:
            self.speak("Good Afternoon")
        else:
            self.speak("Good Evening")
    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Recognizing...")
            qu = r.recognize_google(audio, language='en-in')
            print("Recognised....")
            print("Your Command :  {}\n".format(qu))

        except:
            print("Say that again please...")  
            return ""
        return qu.lower()
    def introduce_yourself(self):
        self.speak("I am {} sir. Please tell me how may i help you".format(self.name))
    def play(self, topic):
        """Will play video on following topic, takes about 10 to 15 seconds to load"""
        url = 'https://www.youtube.com/results?q=' + topic
        count = 0
        cont = requests.get(url)
        data = cont.content
        data = str(data)
        lst = data.split('"')
        for i in lst:
            count+=1
            if i == 'WEB_PAGE_TYPE_WATCH':
                break
        if lst[count-5] == "/results":
            self.speak("No videos found!")
        vid = pafy.new(url)
        video_title = vid.title
        video_author = vid.author
        video_desc = vid.description

        self.speak("Playing "+video_title+" by "+video_author+"")
        print("Video Description : {}".format(video_desc))
        
        web.open("https://www.youtube.com"+lst[count-5])
    def stop(self):
        """
        Stops the assistant by giving a goodbye!
        """
        self.speak("GoodBye Sir! See you later!")
        sys.exit()
    def fetch_news(self):
        try:
            main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey={}'.format(self.news_api_key)
            main_page = requests.get(main_url).json()
            articles = main_page["articles"]
            head = []
            day = ["first", "secend", "third", "fourth", "fifth", "sixth", "seventh", "eight", "ninth", "tenth"]
            for ar in articles:
                head.append(ar["title"])
            for i in range(len(day)):
                self.speak("Today's "+day[i]+" News is "+head[i]+"")
        except Exception as e:
            self.speak("Sorry sir, for the internet issues, i am not able to to fetch the latest news")
    def search(self, squery):
        """
        It will open up the google in the webbrowser and search it!
        """
        link = "https://www.google.com/search?q={}".format(squery)
        web.open(link)
    def get_current_time(self):
        """
        Returns the current time in 12 hour format in string
        """
        time = datetime.datetime.now().strftime("%I:%M %p")
        return time
    def sendEmail(self):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email, self.password)
            self.speak("Sir, what should be the message for the email")
            body = self.takeCommand()
            msg = MIMEMultipart()
            self.speak("What should be the subject for the email")
            subject = self.takeCommand()
            msg['Subject'] = subject
            msg['Body'] = body
            msg['From'] = self.email
            to = input("Enter the email you want to send to: ")
            msg['To'] = to
            text = msg.as_string()

            server.sendmail(self.email, to, text)
            server.quit()
            self.speak("Email has been sent sir")
        except Exception as e:
            self.speak("Sorry sir, i am not able to send the email")

    @property
    def start(self):
        """
        Your assistant will be started by this function!
        """
        self.WishMe()
        self.introduce_yourself()
        while True:
            query = self.takeCommand()
            if 'open youtube' in query:
                self.speak("Ok sir")
                web.open('youtube.com')
            elif 'play' in query:
                video = query.replace('play', '')
                self.play(video)
            elif 'joke' in query:
                list_category = ['neutral', 'chuck']
                category = random.choice(list_category)
                joke = pyjokes.get_joke('en', category)
                self.speak("Heres my joke: {}".format(joke))
            elif 'bye' in query:
                self.stop()
            elif 'stop' in query:
                self.stop()
            elif 'news' in query:
                self.speak("Ok sir, fetching the latest news")
                self.fetch_news()
            elif 'wikipedia' in query:
                q = query.replace('wikipedia', '')
                results = wikipedia.summary(q)
                self.Speak(results)
            elif 'search' in query:
                self.speak("Ok sir")
                squery = query.replace('search', '')
                self.search(squery)
            elif 'time' in query:
                curr_time = self.get_current_time()
                self.speak("Sir, the time is {}".format(curr_time))
            elif 'send email' in query:
                self.sendEmail()