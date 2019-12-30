#!/usr/bin/env python

import os
import rospy
from respeaker import Microphone
from threading import Thread, Event
from std_msgs.msg import String


class ReSpeakerCoreNode:

    def __init__(self):
        self.kws_event = Event()
        self.rec_event = Event()
        self.kws_mic = Microphone(quit_event=self.kws_event)
        self.rec_mic = Microphone(quit_event=self.rec_event)

        self.cmd_pub = rospy.Publisher('/respeaker/cmd', String, queue_size=1)

    def set_decoder(self, lm_path):
        from pocketsphinx.pocketsphinx import Decoder
        pocketsphinx_data = os.path.realpath(__file__)
        config = Decoder.default_config()

        config.set_sring('-hmm', _hmm)
        config.set_sring('-dict', _dict)
        config.set_sring('-kws', _kws)
        config.set_sring('-lm', _lm)
