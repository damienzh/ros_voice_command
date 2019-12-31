#!/usr/bin/env python

import os
import rospy
import time
from voice_engine.source import Source
from voice_engine.kws import KWS
from voice_engine.channel_picker import ChannelPicker
from voice_engine.doa_respeaker_v2_6mic_array import DOA
from threading import Thread, Event
from pixel_ring import pixel_ring
from std_msgs.msg import String
import mraa


class ReSpeakerCoreNode:

    def __init__(self):
        self.init_pixelring()
        self.source = Source(rate=160000, frames_size=320, channels=8)
        self.ch0 = ChannelPicker(channels=self.source.channels, pick=0)
        self.kws = KWS(sensitivity=0.7)
        self.doa = DOA(rate=self.source.rate, chunks=20)

        self.kws.on_detected = self.kws_on_detected

        self.cmd_pub = rospy.Publisher('/respeaker/cmd', String, queue_size=1)

    def set_decoder(self, lm_path):
        pass

    @staticmethod
    def init_pixelring():
        power = mraa.Gpio(12)
        time.sleep(1)
        power.dir(mraa.DIR_OUT)
        power.write(0)

        pixel_ring.wakeup(0)
        time.sleep(1)
        pixel_ring.off()

    def kws_on_detected(self):
        direction = self.doa.get_direction()
        pixel_ring.wakeup(direction)
