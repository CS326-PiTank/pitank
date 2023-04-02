# import time
import RPi.GPIO as GPIO


IN1 = 26
IN2 = 19
IN3 = 13
IN4 = 6
deadzone = 50

GPIO.setmode(GPIO.BCM)  # changes pinout to BCM scheme
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)


def pinCleanUp():
    GPIO.output(IN1, 0)
    GPIO.output(IN2, 0)
    GPIO.output(IN3, 0)
    GPIO.output(IN4, 0)

    GPIO.cleanup()


def pinTest():
    GPIO.output(IN1, 1)
    print("Running IN1 for 3 seconds...")
    GPIO.output(IN1, 0)

    GPIO.output(IN2, 1)
    print("Running IN2 for 3 seconds...")
    GPIO.output(IN2, 0)

    GPIO.output(IN3, 1)
    print("Running IN3 for 3 seconds...")
    GPIO.output(IN3, 0)

    GPIO.output(IN4, 1)
    print("Running IN4 for 3 seconds...")
    GPIO.output(IN4, 0)
# pinTest()


def statereader(leftstate, rightstate):

    # post left tread direction
    if leftstate <= (-1 * deadzone):  # forward
        GPIO.output(IN3, 1)
        GPIO.output(IN4, 0)

    elif leftstate >= deadzone:  # back
        GPIO.output(IN3, 0)
        GPIO.output(IN4, 1)

    else:  # let go of left stick
        GPIO.output(IN3, 0)
        GPIO.output(IN4, 0)

    # post right tread direction
    if rightstate <= (-1 * deadzone):  # forward
        GPIO.output(IN1, 0)
        GPIO.output(IN2, 1)

    elif rightstate >= deadzone:  # back
        GPIO.output(IN1, 1)
        GPIO.output(IN2, 0)

    else:  # let go of right stick
        GPIO.output(IN1, 0)
        GPIO.output(IN2, 0)