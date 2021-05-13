import os

LightingGPIOPin = 7

mycmd = 'gpio write ' + str(LightingGPIOPin) + ' 0' #Turn lights on
os.system(mycmd)