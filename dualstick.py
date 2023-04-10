"""
    dualstick.py

    allows dualstick control of the pitank
"""

__author__ = "Kurt Wietelmann (kaw57), Henry Baldacci (hb43), and Sean Ebenmelu (sce22)"

import RPi.GPIO as GPIO
import time


# GPIO Pins that were used in the Raspberry PI
IN1 = 26
IN2 = 19
IN3 = 13
IN4 = 6

DEADZONE = 50

# GPIO Pins Setup

GPIO.setmode(GPIO.BCM)  # changes pinout to BCM scheme
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)


def pinCleanUp():
    """ GPIO PIN CLEANUP METHOD """

    GPIO.output(IN1, 0)
    GPIO.output(IN2, 0)
    GPIO.output(IN3, 0)
    GPIO.output(IN4, 0)

    GPIO.cleanup()


def pinTest():
    """ Tests the PiTank Tread System """

    GPIO.output(IN1, 1)
    print("Running IN1 for 3 seconds...")
    GPIO.output(IN1, 0)
    time.sleep(3000)

    GPIO.output(IN2, 1)
    print("Running IN2 for 3 seconds...")
    GPIO.output(IN2, 0)
    time.sleep(3000)

    GPIO.output(IN3, 1)
    print("Running IN3 for 3 seconds...")
    GPIO.output(IN3, 0)
    time.sleep(3000)

    GPIO.output(IN4, 1)
    print("Running IN4 for 3 seconds...")
    GPIO.output(IN4, 0)
    time.sleep(3000)

def statereader(leftstate, rightstate):
    """ Reads the trigger response of the controller to determine current state """

    # POST LEFT TREAD DIRECTION
    if leftstate <= (-1 * DEADZONE):    # forward
        GPIO.output(IN3, 1)
        GPIO.output(IN4, 0)

    elif leftstate >= DEADZONE:         # back
        GPIO.output(IN3, 0)
        GPIO.output(IN4, 1)

    else:  # release of left stick
        GPIO.output(IN3, 0)
        GPIO.output(IN4, 0)

    # POST RIGHT TREAD DIRECTION
    if rightstate <= (-1 * DEADZONE):   # forward
        GPIO.output(IN1, 0)
        GPIO.output(IN2, 1)

    elif rightstate >= DEADZONE:        # back
        GPIO.output(IN1, 1)
        GPIO.output(IN2, 0)

    else:  # release of right stick
        GPIO.output(IN1, 0)
        GPIO.output(IN2, 0)