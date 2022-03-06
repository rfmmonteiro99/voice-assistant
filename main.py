# This code is heavily inspired by: Florian Dedov
# (YouTube video: https://www.youtube.com/watch?v=SXsyLdKkKX0)
# Code changed, improved and commented by: Rui Monteiro

from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
import webbrowser
import datetime
import requests
from bs4 import BeautifulSoup
import holidays


# # EXTRA: install PyAudio and download 'omw-1.4'
# import nltk
# nltk.download('omw-1.4')

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)

shopping_list = ['milk', 'eggs', 'chicken breasts', 'sugar', 'orange juice']

def create_note():
    global recognizer

    speaker.say('What do you want to right on your note?')
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say('Choose a filename!')
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()

            with open(f'{filename}.txt', 'w') as f:
                f.write(note)
                done = True
                speaker.say(f'I successfully created the note {filename}')
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say('I did not understand you! Please try again!')
            speaker.runAndWait()

def add_item():
    global recognizer

    speaker.say('What item do you want to add to the shopping list?')
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                shopping_list.append(item)
                done = True

                speaker.say(f'I added {item} to the shopping list!')
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say('I did not understand you! Please try again!')
            speaker.runAndWait()

def show_items():
    speaker.say('The items on your shopping list are the following')
    for item in shopping_list:
        speaker.say(item)
    speaker.runAndWait()

def hello():
    speaker.say('Hello. What can I do for you?')
    speaker.runAndWait()

def quit():
    speaker.say('Goodbye')
    speaker.runAndWait()
    sys.exit(0)

def knock():
    speaker.say("Who's there?")
    speaker.runAndWait()

def yt():
    global recognizer

    speaker.say('What do you want to search on YouTube?')
    speaker.runAndWait()

    with speech_recognition.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        audio = recognizer.listen(mic)

        search_query = recognizer.recognize_google(audio)
        search_query = search_query.lower()
        search_query = search_query.replace(' ', '+')

        webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

def google():
    global recognizer

    speaker.say('What do you want to search on Google?')
    speaker.runAndWait()

    with speech_recognition.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        audio = recognizer.listen(mic)

        search_query = recognizer.recognize_google(audio)
        search_query = search_query.lower()
        search_query = search_query.replace(' ', '+')

        webbrowser.open(f"https://www.google.com/search?q={search_query}")

def christmas():
    date_of_today = datetime.date.today()

    if date_of_today.month == 12 and date_of_today.day == 25:
        speaker.say('Yes, today is December the Twenty Fifth, Christmas Day')
        speaker.runAndWait()
    else:
        speaker.say("No, it is not Christmas Day... Yet!")
        speaker.runAndWait()

def get_daily_news():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find('body').find_all('h3')
    unwanted = ['BBC World News TV', 'BBC World Service Radio', 'News daily newsletter', 
                'Mobile app', 'Get in touch']

    main_headlines = []
    for x in list(dict.fromkeys(headlines)):
        if x.text.strip() not in unwanted:
            main_headlines.append(x.text.strip())

    speaker.say("Today, the main news headlines are:")
            
    main_headlines = main_headlines[:4]
    for headline in main_headlines:
        speaker.say(headline)
        speaker.runAndWait()

def get_holidays():
    # Get today's date
    today = datetime.datetime.today()

    # Get dict with the holidays for this year
    holidays_US = holidays.US(years=today.year)

    # Filter to get only the holidays that will still be celebrated in this year
    holidays_US_filtered = {k: v for k, v in holidays_US.items() if datetime.datetime(k.year, k.month, k.day) > today}

    if holidays_US_filtered == dict():
        speaker.say("This year, there will be no more holidays")
        speaker.runAndWait()

    else:
        speaker.say("This year, the following holidays will be celebrated:")
        for date in holidays_US_filtered.items():
            speaker.say(date[1])
            speaker.runAndWait()


mappings = {
    'greeting': hello,
    'create_note': create_note,
    'add_item': add_item,
    'show_items': show_items,
    'exit': quit,

    'knock': knock,
    'yt': yt,
    'google': google,
    'christmas': christmas,
    'get_daily_news': get_daily_news,
    'get_holidays': get_holidays
}

assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()

            print('Message:\n', message)

        assistant.request(message)

    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
