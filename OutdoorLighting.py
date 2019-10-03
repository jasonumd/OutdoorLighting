# Using the following cron to run this script at 1 am everyday and on system reboot (crontab -e):
# 0 1 * * * /home/pi/OutdoorLighting/OutdoorLighting.py
# @reboot /home/pi/OutdoorLighting/OutdoorLighting.py
# install pip3, python-requests, python-dateutil
# https://www.raspberrypi.org/documentation/linux/usage/cron.md
# https://crontab.guru/#0_19_*_*_*
# https://stackoverflow.com/questions/4770297/convert-utc-datetime-string-to-local-datetime
# https://tecadmin.net/one-time-task-scheduling-using-at-commad-in-linux/
# https://ubuntuforums.org/showthread.php?t=1713092
# http://strftime.org/
# http://pytz.sourceforge.net/

import json
import requests
import time
import datetime
from datetime import timedelta, datetime
import pytz
from pytz import timezone
import os

BufferTimeMinutes = 10
LightingGPIOPin = 7

#Step 1: Get API (UTC) sunrise/sunset times at specified latitude/longitude.
#This is tricky as the api does not return any date info.
#Going to work strictly in UTC.
response = requests.get('https://api.sunrise-sunset.org/json?lat=39.558003&lng=-76.352503')
apidata = response.json()
results = apidata['results']
sunriseApiRawUtc = results['sunrise']
sunsetApiRawUtc = results['sunset']

print('sunriseApiRawUtc: ' + str(sunriseApiRawUtc))
print('sunsetApiRawUtc: ' + str(sunsetApiRawUtc))

#Step 2: Build UTC date/time objects.
nowUtc = datetime.utcnow()
nowUtc = nowUtc.replace(tzinfo = pytz.utc)

print('nowUtc: ' + str(nowUtc))

#Sunrise
sunriseUtc = datetime.strptime(sunriseApiRawUtc, "%I:%M:%S %p")
sunriseUtc = sunriseUtc.replace(year = nowUtc.year, month = nowUtc.month, day = nowUtc.day, tzinfo = pytz.utc)

print('sunriseUtc: ' + str(sunriseUtc))

#Sunset
sunsetUtc = datetime.strptime(sunsetApiRawUtc, "%I:%M:%S %p")
sunsetUtc = sunsetUtc.replace(year = nowUtc.year, month = nowUtc.month, day = nowUtc.day, tzinfo = pytz.utc) #There is a case here where sunsetUtc day is +1 compared to nowUtc

print('sunsetUtc: ' + str(sunsetUtc))

#Buffer
sunriseLightsOffUtc = sunriseUtc + timedelta(minutes = BufferTimeMinutes)
sunsetLightsOnUtc = sunsetUtc - timedelta(minutes = BufferTimeMinutes)

#This is a fix to push the sunset day ahead one day if the UTC time is past midnight. Not too elegant.
if (sunsetLightsOnUtc.hour == 12) or (sunsetLightsOnUtc.hour < 3):
	sunsetLightsOnUtc = sunsetLightsOnUtc + timedelta(days = 1)

print('sunriseLightsOffUtc: ' + str(sunriseLightsOffUtc))
print('sunsetLightsOnUtc: ' + str(sunsetLightsOnUtc))

#Step 3: Set pin to write status. Not sure if it changes with reboot.
mycmd = 'gpio mode ' + str(LightingGPIOPin) + ' out'
os.system(mycmd)

#Step 4: Determine on/off status
blnSunriseLightsOff = False
blnSunsetLightsOn = False

if (nowUtc < sunriseLightsOffUtc): #Turn lights on, need to set turning them on/off. Standard case of the 1 am daily cron.
	print('a')
	mycmd = 'gpio write ' + str(LightingGPIOPin) + ' 1' #Turn lights on
	os.system(mycmd)
	blnSunriseLightsOff = True
	blnSunsetLightsOn = True

elif (nowUtc >= sunriseLightsOffUtc) or (nowUtc < sunsetLightsOnUtc): #Turn lights off, need to set turning them on.
	print('b')
	mycmd = 'gpio write ' + str(LightingGPIOPin) + ' 0' #Turn lights off
	os.system(mycmd)
	blnSunsetLightsOn = True

else: #Just keep lights on. Next 1 am daily cron will handle next day.
	print('c')
	mycmd = 'gpio write ' + str(LightingGPIOPin) + ' 1' #Turn lights on
	os.system(mycmd)
	
#Step 5: Set future on/off in US/Eastern time.
fmt = '%I:%M %p %Y-%m-%d'
est = pytz.timezone('US/Eastern')

if (blnSunriseLightsOff):
	mycmd = 'echo python3 /home/pi/OutdoorLighting/SunriseLightsOff.py | at ' + sunriseLightsOffUtc.astimezone(est).strftime(fmt) #'at -f SunriseLightsOff ' + sunriseLightsOffUtc.astimezone(est).strftime(fmt)
	print(mycmd)
	os.system(mycmd)

if (blnSunsetLightsOn):
	mycmd = 'echo python3 /home/pi/OutdoorLighting/SunsetLightsOn.py | at ' + sunsetLightsOnUtc.astimezone(est).strftime(fmt) #'at -f SunsetLightsOn ' + sunsetLightsOnUtc.astimezone(est).strftime(fmt)
	print(mycmd)
	os.system(mycmd)