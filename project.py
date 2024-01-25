import pvcobra
import pyaudio
import numpy as np
import pvporcupine
import time
import webbrowser
import openai
import json
import requests
import os
import azure.cognitiveservices.speech as speechsdk
import random
from dotenv import load_dotenv


# Keys for different API's
load_dotenv('/mnt/c/Users/VISIONESS/Projects/all-keys.env')

PVCOBRA_KEY = os.environ.get('PVCOBRA_API_KEY')
OPENAPI_KEY = os.environ.get('OPENAPI_KEY')
OPENWEATHER_KEY = os.environ.get('OPEN_WEATHER_API_KEY')
SPEECH_KEY = os.environ.get('SPEECH_KEY')


os.system("cls")
print("\n\nLoading Friday...")

# Loading pvcobra(speech detection), pvporcupine(wake word detection), openai's chatgpt, microsoft azure(speech to text(speech recognition)), microsoft azure(text to speech)
handle = pvcobra.create(access_key=PVCOBRA_KEY)
porcupine = pvporcupine.create(access_key=PVCOBRA_KEY, keyword_paths=[r"C:\Users\VISIONESS\Projects\cs50-final\projectenv\project\Friday_en_windows_v3_0_0.ppn", r"C:\Users\VISIONESS\Projects\cs50-final\projectenv\project\Shut-down_en_windows_v3_0_0.ppn"])
openai.api_key = OPENAPI_KEY

speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region='westeurope')
speech_config.speech_recognition_language="en-US"

audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Define the audio parameters needed for pvcobra
sample_rate = int(handle.sample_rate)
frame_length = int(handle.frame_length)


def main():
    try:
        
        text_to_speech("You can say 'Friday' to wake me up!")
        while True:
            # Opening a stream to get voice from microphone
            stream = get_stream()
            audio_frame = get_next_audio_frame(stream)
            # If any keyword("Friday", "Shut Down") is called it executes its own function
            keyword_index = porcupine.process(audio_frame)
            # "Friday"
            if keyword_index == 0:
                os.system("cls")
                print("""\n\n    
                \t\t\t ███████████            ███      █████                     
                \t\t\t░░███░░░░░░█           ░░░      ░░███                      
                \t\t\t ░███   █ ░  ████████  ████   ███████   ██████   █████ ████
                \t\t\t ░███████   ░░███░░███░░███  ███░░███  ░░░░░███ ░░███ ░███ 
                \t\t\t ░███░░░█    ░███ ░░░  ░███ ░███ ░███   ███████  ░███ ░███ 
                \t\t\t ░███  ░     ░███      ░███ ░███ ░███  ███░░███  ░███ ░███ 
                \t\t\t █████       █████     █████░░████████░░████████ ░░███████ 
                \t\t\t░░░░░       ░░░░░     ░░░░░  ░░░░░░░░  ░░░░░░░░   ░░░░░███ 
                \t\t\t                                                  ███ ░███ 
                \t\t\t                                                 ░░██████  
                \t\t\t                                                  ░░░░░░  
                    """)
                text_to_speech("I'm setting up my utils...")
                text_to_speech(f"Listening to you {calluser()}")
                # After waking up "Friday", it will now listen to us until we talk
                while True:
                    voice_probability = 0
                    # Opening a stream again
                    streamn = get_stream()
                    for _ in range(10):
                        handle.process(get_next_audio_frame(streamn))
                    # Checking if there's any speech by pvcobra, if there is it breaks the loop
                    while voice_probability < 0.5:
                        voice_probability = handle.process(get_next_audio_frame(streamn))
                    
                    # Speech to text conversion
                    task = recognize_from_microphone()
                    # Closing stream to get any possible voice detection errors (Still got some problems about it!)
                    streamn.close()

                    print("\n-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-\n\nMe --", task, "\n")

                    # If "sleep mode" wanted, goes back to waiting for wake up word
                    if "sleep mode" in task:
                        text_to_speech(f"Going for the sleep mode {calluser()}! Wake me up again by saying 'Friday' when you need me.")
                        break 
                    # Getting response and conversion from text to speech 
                    text_to_speech(get_response(task))
                            
            # "Shut Down"           
            if keyword_index == 1:
                text_to_speech(f"Shutting down the system {calluser()}!\n")
                release_resources(stream)
                break

    except KeyboardInterrupt:
        pass

# Randomly calling user with one of these titles
def calluser():
    return random.choice(["boss", "Mr.", "sir"])

# Creating a stream for the audio
def get_stream():
    stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=sample_rate,
                input=True,
                frames_per_buffer=frame_length)
    return stream

# Getting next audio frame to process
def get_next_audio_frame(stream):
    audio_data = np.frombuffer(stream.read(frame_length), dtype=np.int16)
    return audio_data

# Text to speech conversion by Azure
def text_to_speech(text):
    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name='en-GB-LibbyNeural'
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    print("\nFriday -- ", text)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print()
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print(cancellation_details.reason)
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print(cancellation_details.error_details)

# Speech to text conversion by Azure
def recognize_from_microphone():
    print("\nListening...")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        # Returning the text result instead of printing because we send it as a parameter to the text_to_speech function
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
    return "Error at getting audio"

# Opening any site that user wants but it must include 'https://www.' and '.com'
def open_site(site):
    webbrowser.open_new(f"https://www.{site}.com")
    return f"Opening {site} {calluser()}!"

# Creating file if it does not exist, after creating it writing in it if needed
def create_file(filename, extension):
    with open(f"C:\\Users\\VISIONESS\\Projects\\cs50-final\\projectenv\\{filename}.{extension}", "a") as f:
        text_to_speech("Do you want me to write anything in the file?")
        answer = recognize_from_microphone().lower()
        if "yes" in answer or "sure" in answer or "yeah" in answer:
            text = recognize_from_microphone()
            f.write("\n" + text)
            text_to_speech(f"I wrote those to the file. Would you like to add more {calluser()}?")
            answer2 = recognize_from_microphone().lower()
            if "yes" in answer2 or "sure" in answer2 or "yeah" in answer2:
                text = recognize_from_microphone()
                f.write("\n" + text)
                return "Added these to created file."
        return f"File is created {calluser()}!"

# Reading file if the file exist
def read_file(filename, extension):
    try:
        with open(f"C:\\Users\\VISIONESS\\Projects\\cs50-final\\projectenv\\{filename}.{extension}", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "There's no file with given filename and extension"

# Getting current weather data from openweather for given location
def get_weather(location):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_KEY}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return (f"Weather in {location}: {data['weather'][0]['description']}\nTemperature: {data['main']['temp']}°C")
    else:
        return "Failed to fetch weather data."

# Sending the task to chatgpt as a prompt, also checking if there is any related function for this prompt
# If there is one, for example 'get_weather' for 'How is the weather today in Antalya' it calls the related function and returns its result as a response
# Also if any parameter is missing for calling any function, sends a response to user to provide needed parameters
# If not, it just creates a response for it and returns that
def get_response(task):
    # It does not remember previous conversations because I had limited tokens to use ChatGPT
    # Also we send a system message to it everytime we have a task for it, because it should know what's the name or purpose of 'Friday' or its creator
    messages = [{"role": "system", "content": "You are a helpful voice assistant named 'Friday' which is created by 'Aygun Servet Zurnaci' as a final project for CS50 from Harvard. Your profession is generally computer science."},
                {"role": "user", "content": task}]
    
    # Defining functions for GPT
    functions = [
        {
            "name": "open_site",
            "description": "Open the website or app",
            "parameters": {
                "type": "object",
                "properties": {
                    "site": {
                        "type": "string",
                        "description": "Website or app",
                    },
                },
            },
        },
        {
            "name": "get_weather",
            "description": "Gets the current weather for the given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location for the current weather"
                    },
                },
                "required": ["location"],
            },
        },
        {
            "name": "create_file",
            "description": "Creates a file with given filename and extension",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name of the file that is creating",
                    },
                    "extension": {
                        "type": "string",
                        "description": "Extension of the file like 'exe|md|py'",
                    },
                },
                "required": ["filename", "extension"],
            },   
        },
        {
            "name": "read_file",
            "description": "Reads a file with given filename and extension",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name of the file that is creating",
                    },
                    "extension": {
                        "type": "string",
                        "description": "Extension of the file like 'exe|md|py'",
                    },
                },
                "required": ["filename", "extension"],
            },
        },
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    response_message = response["choices"][0]["message"]

    # Checking if GPT wanted to call a function
    if response_message.get("function_call"):
        # Calling the appropriate function
        available_functions = {
            "open_site": open_site,
            "get_weather": get_weather,
            "create_file": create_file,
            "read_file": read_file,
        }
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(**function_args)

        # Sending the info on the function call and function response to GPT
        return function_response

    # Extract and print the assistant's reply if no function called
    assistant_reply = response['choices'][0]['message']['content']
    return assistant_reply


# Releasing resources while shutting down
def release_resources(stream):
    stream.stop_stream()
    stream.close()
    p.terminate()
    porcupine.delete()
    handle.delete()


if __name__ == "__main__":
    main()