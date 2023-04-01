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
