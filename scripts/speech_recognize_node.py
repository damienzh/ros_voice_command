import rospy
import os
import speech_recognition as sr
from std_msgs.msg import String
from std_srvs.srv import Trigger, TriggerResponse


class ROSSpeechRecognizer:

    def __init__(self, mic_idx=0):
        self.mic_list = []
        self.Recognizer = sr.Recognizer()
        self.Mic = sr.Microphone(device_index=mic_idx)
        self.language = 'en-US'
        self.kws = None

        self.result_pub = rospy.Publisher('/speech_recognizer/result', String, queue_size=5)
        self.recognize_srv = rospy.Service('/speech_recognizer/listen', Trigger, self.listen_hdl)

    def get_microphone_list(self):
        self.mic_list = sr.Microphone.list_microphone_names()

    def recognize_sphinx(self):
        with self.Mic as source:
            self.Recognizer.adjust_for_ambient_noise(source, duration=1)
            print "listening..."
            audio = self.Recognizer.listen(source, phrase_time_limit=3)
            try:
                msg = self.Recognizer.recognize_sphinx(audio, language=self.language, keyword_entries=self.kws)
                ret = True
                print('Sphinx thinks you said:'.format(msg))
            except sr.UnknownValueError:
                print('Sphinx could not understand audio')
                msg = 'Could not understand'
                ret = False
            except sr.RequestError as e:
                print('Sphinx error:{}'.format(e))
                msg = e
                ret = False
        return ret, msg

    def set_language(self, model_name):
        p = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
        base_path = os.path.join(p, 'param', model_name)
        hmm_path = os.path.join(base_path, model_name + '.cd_cont_5000')
        lm_file = os.path.join(base_path, model_name + '.lm.bin')
        dic_file = os.path.join(base_path, model_name + '.dic')

        self.language = (hmm_path, lm_file, dic_file)

    def listen_hdl(self, req):
        response = TriggerResponse()
        r, msg = self.recognize_sphinx()
        if r:
            response.success = r
            response.message = msg
            s = String()
            s.data = msg
            self.result_pub.publish(s)
        else:
            response.success = r
            response.message = msg
        return response


if __name__ == '__main__':
    rospy.init_node('speech_recognizer')
    sr = ROSSpeechRecognizer()