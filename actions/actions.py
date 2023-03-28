# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

# import wav2letter as w2l
# import torch
# import torchaudio
# import numpy as np
# import os
# import json
# import time
# import requests
# function to get live audio from microphone
def get_audio():
     # get audio from microphone
    r = requests.get('http://localhost:5000/audio')
    audio = r.content
    return audio
# save audio to file
    with open('audio.wav', 'wb') as f:
        f.write(audio)
    # load audio from file
    audio, sr = torchaudio.load('audio.wav')
    return audio, sr
# function to get text from audio
def get_text(audio):
# get text from audio
    text = model.decode(audio)
    return text
# function to get intent from text
def get_intent(text):
        # get intent from text
    intent = model.interpreter(text)
    return intent
# function to get response from intent
def get_response(intent):
    # get response from intent
    response = model.interpreter(intent)
    return response
# function to send response to user
def send_response(response):
        # send response to user
    print(response)
# function to get action from intent
def get_action(intent):
        # get action from intent
    action = model.interpreter(intent)
    return action
# function to run action
def run_action(action):
        # run action
    model.interpreter(action)
# function to convert live audio to text
def audio_to_text():
        # get audio from microphone
    audio = get_audio()
        # get text from audio
    text = get_text(audio)
    return text
