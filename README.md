# OutdoorLighting
Python scripts used to automatically turn outdoor lighting on/off from a Raspberry Pi. Utilizes the Sunrise Sunset REST API to return times in JSON (https://sunrise-sunset.org/). Updated code pulls a better formatted JSON file which includes the date and insists the Pi operate in UTC mode.
<br>
Uses the following packges:<br>
Set the pi to utilize UTC (sudo raspi-config, Localisation Options, Timezone, None of the Above, UTC)<br>
Enable GPIO pins (sudo raspi-config, Interface Options, I2C, Yes) (sudo raspi-config, Interface Options, SPI, Yes)<br>
sudo apt-get install python3-pip<br>
sudo apt-get install at<br>
pip3 install requests<br>
pip3 install python-dateutil<br>
pip3 install pytz<br>
<br>
Using the following cron to run this script at 2 am everyday and on system reboot (crontab -e):<br>
0 2 * * * /home/pi/OutdoorLighting/OutdoorLighting.py<br>
@reboot /home/pi/OutdoorLighting/LightsOff.py<br>
@reboot /home/pi/OutdoorLighting/OutdoorLighting.py<br>
<br>
chmod +x OutdoorLighting.py
chmod +x LightsOff.py
chmod +x LightsOn.py
