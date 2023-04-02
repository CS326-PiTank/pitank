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
import numpy as np
import paho.mqtt.client as mqtt


class Stream_receiver:

    def __init__(self, topic='', host="host", port=8883):
        """
        Construct a new 'stream_receiver' object to retreive a video stream using Mosquitto_MQTT

        :param topic: MQTT topic to send Stream         
        :param host:  IP address of Mosquitto MQTT Broker
        :param Port:  Port at which Mosquitto MQTT Broker is listening

        :return: returns nothing

        : use " object.frame  "  it contains latest frame received
        """
        CERTS = '/etc/ssl/certs/ca-certificates.crt'
        self.topic = topic
        self.frame = None  # empty variable to store latest message received

        self.client = mqtt.Client()  # Create instance of client
        self.client.username_pw_set('username', password='password')
        self.client.tls_set(CERTS)
        # Define callback function for successful connection
        self.client.on_connect = self.on_connect
        self.client.message_callback_add(self.topic, self.on_message)

        self.client.connect(host, port)  # connecting to the broking server

        # make a thread to loop for subscribing
        t = threading.Thread(target=self.subscribe)
        t.start()  # run this thread

    def subscribe(self):
        self.client.loop_forever()  # Start networking daemon

    # The callback for when the client connects to the broker
    def on_connect(self, client, userdata, flags, rc):
        # Subscribe to the topic, receive any messages published on it
        client.subscribe(self.topic)
        print("Subscribing to topic :", self.topic)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):

        nparr = np.frombuffer(msg.payload, np.uint8)
        self.frame = cv2.imdecode(nparr,  cv2.IMREAD_COLOR)

        # frame= cv2.resize(frame, (640,480))   # just in case you want to resize the viewing area
        cv2.imshow('PiTank Monitor', self.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return


if __name__ == "__main__":
    # creating 4 instances of the MQ_subs class
    j = Stream_receiver(topic="picar")
