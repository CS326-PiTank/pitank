#!/usr/bin/env python
"""Stream_publisher.py: Send video stream via Mosquitto Mqtt topic """

__author__ = "Jatin Goyal"
__copyright__ = "Copyright 2022, Video surveillance Project"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Jatin Goyal"
__email__ = "robojatin@gmail.com"
__status__ = "Production"

import cv2
import threading
import paho.mqtt.client as mqtt
import imutils


class Stream_publisher:

    def __init__(self, topic, video_address=0, start_stream=True, host="host", port=8883) -> None:
        """
        Construct a new 'stream_publisher' object to broadcast a video stream using Mosquitto_MQTT

        :param topic: MQTT topic to send Stream
        :param video_address: link for OpenCV to read stream from, default 0 (webcam)

        :param start_stream:  start streaming while making object, default True, else call object.start_streaming()

        :param host:  IP address of Mosquitto MQTT Broker
        :param Port:  Port at which Mosquitto MQTT Broker is listening

        :return: returns nothing
        """
        CERTS = '/etc/ssl/certs/ca-certificates.crt'
        self.client = mqtt.Client()  # create new instance
        self.client.username_pw_set('username', password='password')
        self.client.tls_set(CERTS)
        self.client.connect(host, port)
        self.topic = topic
        self.video_source = video_address

        self.state = False  # whether camera is on or off
        self.last_button = False  # keep track of last button state to avoid digital bouncing

        self.cam = cv2.VideoCapture(self.video_source)

        self.streaming_thread = threading.Thread(target=self.stream)
        if start_stream:
            self.streaming_thread.start()

    def start_streaming(self):
        self.streaming_thread.start()

    def stream(self):
        print("Streaming from video source : {}".format(self.video_source))
        while True:
            # if self.state:
            _, img = self.cam.read()
            flippedimg = imutils.rotate(img, angle=180)
            img_str = cv2.imencode('.jpg', flippedimg)[1].tobytes()

            self.client.publish(self.topic, img_str, qos=0)

    def updateState(self, button):
        if button != self.last_button:
            self.last_button = button
            if button == 1:
                self.state = not self.state


if __name__ == "__main__":
    # streaming from webcam (0) to  topic : "test"
    webcam = Stream_publisher("picar", video_address=0)
    # file= Stream_publisher("test", video_address="kungfu-panda.mkv")  # streaming from a file to  topic : "test"
