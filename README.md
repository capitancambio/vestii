# Intro

code for the hack the senses hackathon

VestiiInterface.py is the control program. Updates to the current and
polarity values will be made and fed into a Vestii object. These are 
then sent via serial connection to Vestii.

Should be entirely self contained, will interpret any list of current 
and polarity values that is pushed into it.

Myo side of the project outputs CSV of accelerometer data, this will 
then be interpreted and converted into polarity and current.