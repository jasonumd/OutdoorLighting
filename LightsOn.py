import os

LightingGPIOPin = 7

mycmd = 'gpio write ' + str(LightingGPIOPin) + ' 1' #Turn lights on
os.system(mycmd)