import sys
sys.path.append("..")
import VestiiInterface
#export DYLD_LIBRARY_PATH='/Users/David/PycharmProjects/vestii/Myo/MyoSDK/myo.framework'

from time import sleep
from myo import init, Hub, DeviceListener
import os
import platform

if platform.system() == 'Darwin':
    os.environ["DYLD_LIBRARY_PATH"] = '/Users/David/PycharmProjects/vestii/Myo/MyoSDK/myo.framework'

class Listener(DeviceListener):

    def __init__(self, vestii):
        self.max_x = -1001
        self.min_x = 1000
        self.max_y = -1001
        self.min_y = 1000
        self.vestii = vestii

    def on_pair(self, myo, timestamp, firmware_version):
        print("Hello, Myo!")

    def on_orientation_data(self, myo, timestamp, quat):
        norm_x = 0
        norm_y = 0
        orientation_values = [quat.x, quat.y, quat.z, quat.w]
        if quat.x > self.max_x:
            self.max_x = quat.x
        if quat.x <= self.min_x :
            self.min_x = quat.x
        if quat.y > self.max_y:
            self.max_y = quat.y
        if quat.y <= self.min_y:
            self.min_y = quat.y
        if self.max_x != self.min_x:
            norm_x = (self.max_x - quat.x) / (self.max_x - self.min_x)

        if self.max_y != self.min_y:
            norm_y = (self.max_y - quat.y) / (self.max_y - self.min_y)




        polarity = 1 if norm_x > 0.5 else 0
        current = int(255 * norm_y)
        print "Current %d Polarity %d(%f)"%(current,polarity,norm_x)
        self.vestii.UpdateVestii([polarity,0],[current,0])




init()
hub = Hub()
hub.run(1000, Listener(VestiiInterface.Vestii()))
try:
    while True:
        sleep(0.5)
except KeyboardInterrupt:
    print('\nQuit')
finally:
    hub.shutdown()  # !! crucial