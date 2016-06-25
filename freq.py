# import numpy as np
import VestiiInterface
import time

polarties = [0, 0]
vals = [40, 200]

vesti = VestiiInterface.Vestii()

idx = 0
print "Synchronised"
while 10:
    time.sleep(2)
    vesti.UpdateVestii(polarties, [vals[idx], vals[idx]])
    idx += 1
    idx = idx % 2

print "Alternating"
while 10:
    time.sleep(2)
    vesti.UpdateVestii(polarties, [vals[idx], vals[(idx + 1) % 2]])
    idx += 1
    idx = idx % 2
