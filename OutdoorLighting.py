# Using the following cron to run this script at 2 am UTC everyday and on system reboot (crontab -e):
# 0 2 * * * /home/pi/OutdoorLighting/OutdoorLighting.py
# @reboot /home/pi/OutdoorLighting/LightsOff.py
# @reboot /home/pi/OutdoorLighting/OutdoorLighting.py

# chmod +x OutdoorLighting.py
# chmod +x LightsOff.py
# chmod +x LightsOn.py

# Set the pi to utilize UTC (sudo raspi-config, Localisation Options, Timezone, None of the Above, UTC)
# Enable GPIO pins (sudo raspi-config, Interface Options, I2C, Yes) (sudo raspi-config, Interface Options, SPI, Yes)
# sudo apt-get install python3-pip
# sudo apt-get install at
# pip3 install requests
# pip3 install python-dateutil
# pip3 install pytz
# https://www.raspberrypi.org/documentation/linux/usage/cron.md
# https://crontab.guru/#0_19_*_*_*
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
myCmdLightsOn = '/home/pi/OutdoorLighting/LightsOn.py'
myCmdLightsOff = '/home/pi/OutdoorLighting/LightsOff.py'

#Step 1: Get now.
nowUtc = datetime.utcnow() #Could also use now() as the pi will operate in UTC.
nowUtc = nowUtc.replace(tzinfo = pytz.utc)
print('nowUtc: ' + str(nowUtc))

#Step 2: Get API (UTC) sunrise/sunset times at specified latitude/longitude.
#Going to work strictly in UTC.
response = requests.get('https://api.sunrise-sunset.org/json?lat=39.558003&lng=-76.352503&formatted=0', verify=False)
apidata = response.json()
results = apidata['results']
sunriseApiRawUtc = results['sunrise']
sunsetApiRawUtc = results['sunset']

#Sunrise
#Raw data will look like "2021-05-12T09:52:58+00:00"
print('sunriseApiRawUtc: ' + str(sunriseApiRawUtc))
sunriseUtc = datetime.strptime(sunriseApiRawUtc, "%Y-%m-%dT%H:%M:%S+00:00")
sunriseUtc = sunriseUtc.replace(tzinfo = pytz.utc)
print('sunriseUtc: ' + str(sunriseUtc))

#Sunset
print('sunsetApiRawUtc: ' + str(sunsetApiRawUtc))
sunsetUtc = datetime.strptime(sunsetApiRawUtc, "%Y-%m-%dT%H:%M:%S+00:00")
sunsetUtc = sunsetUtc.replace(tzinfo = pytz.utc)
print('sunsetUtc: ' + str(sunsetUtc))

#Buffer
sunriseLightsOffUtc = sunriseUtc + timedelta(minutes = BufferTimeMinutes)
sunsetLightsOnUtc = sunsetUtc - timedelta(minutes = BufferTimeMinutes)

print('sunriseLightsOffUtc: ' + str(sunriseLightsOffUtc))
print('sunsetLightsOnUtc: ' + str(sunsetLightsOnUtc))

#Step 4: Turn lights on if the system is rebooted during period when they should be on.
if (nowUtc < sunriseLightsOffUtc) or (nowUtc > sunsetLightsOnUtc): #Turn lights on, need to set turning them on/off. Standard case of the 1 am daily cron.
    print('Turning on lights that should be on')
    os.system(myCmdLightsOn)

#Step 5: Set future off/on in UTC.
fmt = '%H:%M %Y-%m-%d'

#If rebooted, these times could be in the past in which case the cmd will error out but not cause problems.
myCmd = myCmdLightsOff + ' | at ' + sunriseLightsOffUtc.strftime(fmt)
print(myCmd)
os.system(myCmd)


myCmd = myCmdLightsOn + ' | at ' + sunsetLightsOnUtc.strftime(fmt)
print(myCmd)
os.system(myCmd)
