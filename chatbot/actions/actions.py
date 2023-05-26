# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from pymongo import MongoClient
from pymongo.collection import Collection
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Any, Dict, List, Text
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json

class ActionHelloWorld(Action):

     def name(self) -> Text:
         return "action_hello_world"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message(text="Hello World!")

         return []


# Assuming you have already initialized the MongoDB client
client = MongoClient('mongodb://localhost:27017')
db = client['hospital_data']

class ActionGetDoctors(Action):
    def name(self) -> Text:
        return "action_get_doctors"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        hospital_name = tracker.get_slot("hospital_name")  # Assuming the value is obtained from a slot
        if not isinstance(hospital_name, str):
            # Handle the case when hospital_name is not a string
            # Assign a default value or raise an exception, depending on your use case
            raise ValueError("hospital_name must be a string ",hospital_name)
        hospital_name = hospital_name.upper()  # Convert to uppercase to match the collection name
        collection = db[hospital_name]  # Access the collection using the string value
        doctor_specialty = tracker.get_slot('general_practitioner')
        'change doctor_specialty to lowercase'
        doctor_specialty = doctor_specialty.lower()

        try:
            # Query the collection to retrieve doctors with the specified specialty
            doctors = collection.find({'specialist': doctor_specialty})

            # Build a list of doctor names
            doctor_names = [doctor['name'] for doctor in doctors]
            print(doctor_names)

            if len(doctor_names) > 0:
                # Send the doctor names as buttons for the user to select
                dispatcher.utter_message(text="Here are the available doctors:")
                buttons = [{'title': name, 'payload': json.dumps({'doctor_name': name})} for name in doctor_names]
                buttons = [button['title'].strip() for button in buttons]
                buttons_string = '\n'.join(buttons)
                dispatcher.utter_message(buttons_string)

            else:
                dispatcher.utter_message(text=f"No doctors found with the specified specialty {doctor_specialty}.")

        except ConnectionFailure:
            dispatcher.utter_message(text="Could not connect to the database.")

        return []

'''
import os
import requests
import speech_recognition as sr
import soundfile as sf
import torch
import torchaudio
from speechbrain.pretrained import EncoderDecoderASR

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher


class ActionCaptureAudio(Action):
    def name(self):
        return "action_capture_audio"

    def run(self, dispatcher, tracker, domain):
        # Start capturing live audio
        r = sr.Recognizer()
        mic = sr.Microphone()

        # Prompt user to speak
        dispatcher.utter_message(text="I'm listening...")
        
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            dispatcher.utter_message(text="Got it! Now processing...")
        
        # Save audio to file
        audio_file = "live_audio.wav"
        with open(audio_file, "wb") as f:
            f.write(audio.get_wav_data())

        # Transcribe audio using SpeechBrain
        asr_model = EncoderDecoderASR.from_hparams(source="speechbrain/asr-crdnn-rnnlm-librispeech", savedir="pretrained_models/asr-crdnn-rnnlm-librispeech")
        waveform, sample_rate = torchaudio.load(audio_file)
        transcript = asr_model.transcribe_batch([waveform], [sample_rate])[0]

        # Set slot with transcribed text
        return [SlotSet("captured_audio", transcript)]


class ActionGenerateResponse(Action):
    def name(self):
        return "action_generate_response"

    def run(self, dispatcher, tracker, domain):
        # Get transcribed text from slot
        captured_audio = tracker.get_slot("captured_audio")

        # Generate response based on captured audio
        response = "You said: {}".format(captured_audio)

        dispatcher.utter_message(text=response)
        return []
'''
