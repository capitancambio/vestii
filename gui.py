import Tkinter as tk
import VestiiInterface
import Leap
import sys


class State(object):

    def __init__(self, vestii):
        self.currents = [0., 0.]
        self.polarities = [0., 0.]
        self.vestii = vestii
        self.LeapList = []
        for y in range(0, 11):
            self.LeapList.append((255 / 10) * y)

    def update_current_1(self, event):
        self.currents[0] = int(event)
        print "Updated currents", self.currents
        self.update_vestii()

    def update_current_2(self, event):
        self.currents[1] = int(event)
        print "Updated currents", self.currents
        self.update_vestii()

    def update_polarity_1(self, ):
        self.polarities[0] = (self.polarities[0] + 1) % 2
        print "Updated polarities", self.polarities
        self.update_vestii()

    def update_polarity_2(self):
        self.polarities[1] = (self.polarities[1] + 1) % 2
        print "Updated polarities", self.polarities
        self.update_vestii()

    def update_vestii(self):
        self.vestii.UpdateVestii(self.polarities, self.currents)

    def LeapControl(self, CurPos):
        self.currents[0] = self.LeapList[CurPos]
        self.currents[1] = self.LeapList[CurPos]
        self.update_vestii()

    def Reset(self):
        self.vestii.ZeroVestii()
        self.currents = [0, 0]
        print "Updated currents", self.currents


class ShapeListener(Leap.Listener):

    def on_connect(self, controller):
        print "Connected"
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        self.CurrentPos = 1

    def on_frame(self, controller):
        global InitXPos
        global FinalXPos

        frame = controller.frame()

        for gesture in frame.gestures():
            if gesture.type is Leap.Gesture.TYPE_CIRCLE:
                circle = Leap.CircleGesture(gesture)
                if circle.state == 3:
                    ShapePos = 1
                    SHAPE.ShapeClassMenu(shapecircle, ShapePos)

        for gesture in frame.gestures():
            if gesture.type is Leap.Gesture.TYPE_SWIPE:
                swipe = Leap.SwipeGesture(gesture)
                if swipe.state == 1:
                    InitXPos = swipe.direction

                if swipe.state == 3:
                    FinalXPos = swipe.direction
                    DeltaX = float(FinalXPos[0]) - float(InitXPos[0])

                    if DeltaX < 0:
                        if self.CurrentPos >= 1:
                            self.CurrentPos = self.CurrentPos - 1
                        else:
                            self.CurrentPos = 0

                    else:
                        if self.CurrentPos <= 10:
                            self.CurrentPos = self.CurrentPos + 1
                        else:
                            self.CurrentPos = 11
                    state.LeapControl(self.CurrentPos)

        for gesture in frame.gestures():
            if gesture.type is Leap.Gesture.TYPE_KEY_TAP:
                tap = Leap.KeyTapGesture(gesture)
                state.Reset()
                self.CurrentPos = 0


class SHAPE():

    def Circle(self):
        print('Circular activation')

    def ShapeClassMenu(self, Num):

        if Num == 1:
            SHAPE.Circle(shapemenu)

    def Reset(self):
        print('Nothing')


def ShapeMotionSense():
    print('This mode uses the Leap Motion to translate some movements into commands:' + '\n')
    print('Swipe left or right to change between shapes' + '\n')
    listener = ShapeListener()
    controller = Leap.Controller()
    controller.add_listener(listener)

    print "Press Enter to stop..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)


shapemenu = SHAPE()
shapecircle = SHAPE()
shapeswipe = SHAPE()
shaperandom = SHAPE()
state = State(VestiiInterface.Vestii())
root = tk.Tk()

root.geometry("%dx%d" % (200, 200))
current_1 = tk.Scale(root, from_=0, to=255, command=state.update_current_1)
current_1.grid(row=0, column=0)
polarity_1 = tk.Checkbutton(root, text="Polarity 1",
                            command=state.update_polarity_1)
polarity_1.grid(row=1, column=0)

current_2 = tk.Scale(root, from_=0, to=255, command=state.update_current_2)
current_2.grid(row=0, column=1)
polarity_2 = tk.Checkbutton(root, text="Polarity 2",
                            command=state.update_polarity_2)
polarity_2.grid(row=1, column=1)

button1 = tk.Button(root, text="Leap", command=ShapeMotionSense)
button1.grid(row=7, column=0)

button2 = tk.Button(root, text="Exit", command=sys.exit)
button2.grid(row=7, column=1)

button3 = tk.Button(root, text="Reset", command=state.Reset())
button3.grid(row=8, column=1)

root.mainloop()
