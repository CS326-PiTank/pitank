"""
controller.py

driver code for the piTank

Adapted from: https://gist.github.com/effedebe/6cae2a5849923fb373ab749594b9ed50
"""

___author___ = "Henry Baldacci (hb43), Kurt Wietelmann (kaw57), and Sean Ebenmelu (sce22)"
___copyright__ = "Copyright 2018 Francois De Bue"


from threading import Thread
from inputs import get_gamepad
import dualstick
from Stream_publisher import Stream_publisher


class XPAD(Thread):				# def class typr thread
    """
        sdf
    """
    def __init__(self):
        Thread.__init__(self)		# thread init class (don't forget this)
        self.A = 0			        # all vars of gamepad, set init val to 0
        self.B = 0
        self.X = 0
        self.Y = 0
        self.LBumper = 0
        self.RBumper = 0
        self.LThumb = 0
        self.RThumb = 0
        self.LTrigger = 0
        self.RTrigger = 0
        self.Back = 0
        self.Start = 0
        self.LStickX = 0
        self.LStickY = 0
        self.RStickX = 0
        self.RStickY = 0
        self.DPadX = 0
        self.DPadY = 0

        self.Stream = Stream_publisher("picar", video_address=0)

    def run(self):		# run is a default Thread function
        """ run method constantly checks which button event is being triggered """

        while True:  # loop for ever
            for event in get_gamepad():  # check events of gamepads, if not event, all is stop
                if event.ev_type == "Key":  # category of binary respond values
                    if event.code == "BTN_SOUTH":
                        self.A = event.state
                    elif event.code == "BTN_EAST":
                        self.B = event.state
                    elif event.code == "BTN_WEST":
                        self.X = event.state
                    elif event.code == "BTN_NORTH":
                        self.Y = event.state
                    elif event.code == "BTN_TL":
                        self.LBumper = event.state
                    elif event.code == "BTN_TR":
                        self.RBumper = event.state
                    elif event.code == "BTN_THUMBL":
                        self.LThumb = event.state
                    elif event.code == "BTN_THUMBR":
                        self.RThumb = event.state
                    elif event.code == "BTN_START":
                        self.Back = event.state
                    elif event.code == "BTN_SELECT":
                        self.Start = event.state

                elif event.ev_type == "Absolute":  # category of analog values
                    # some values are from -32000 to 32000, or -256 to 256
                    # here all values are mapped from -512 to 512 by bitshifting
                    if event.code[-1:] == "Z":
                        event.state = event.state << 1  # reduce range from 256 to 512
                    else:
                        event.state = event.state >> 6  # reduce range from 32000 to 512

                    if event.state < 40 and event.state > -40:  # dead zone of my joypad, check this one for yours
                        event.state = 0

                    if event.code == "ABS_Z":
                        self.LTrigger = event.state
                    elif event.code == "ABS_RZ":
                        self.RTrigger = event.state
                    elif event.code == "ABS_X":
                        self.LStickX = event.state
                    elif event.code == "ABS_Y":
                        self.LStickY = event.state
                    elif event.code == "ABS_RX":
                        self.RStickX = event.state
                    elif event.code == "ABS_RY":
                        self.RStickY = event.state
                    elif event.code == "ABS_HAT0Y":
                        self.DPadX = event.state
                    elif event.code == "ABS_HAT0X":
                        self.DPadY = event.state

            dualstick.statereader(self.LStickY, self.RStickY)


def main():
    ''' with gamepad thread, count continue all the time '''

    gamePad = XPAD()    # creation thread joypad
    count = 0		    # count represent continuity of your code
    gamePad.start() 	# start of gamepad thread, to read input of game pad (multitasking forever)

    while True:
        try:

            count = count + 1 	# your code

            if gamePad.A != 0: 	# your interaction
                count = count - 100
                # print("Count value: {}").format(count)

            # print(count)

        except KeyboardInterrupt:
            dualstick.pinCleanUp()  # cleans up GPIO pins that are used in runtime
            gamePad.join() 		    # wait the end of joypad thread
            print("Operation Done")
            exit(1)


if __name__ == "__main__":
    main()
