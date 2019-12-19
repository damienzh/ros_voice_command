import rospy
import speech_recognition as sr


class ROSSpeechRecognizer:

    def __init__(self, mic_idx=0):
        self.Recognizer = sr.Recognizer()
        self.Mic = sr.Microphone(device_index=mic_idx)
        self.language = 'en-US'

    def get_microphone_list(self):
        self.mic_list = sr.Microphone.list_microphone_names()
