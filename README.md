# OutdoorLighting
Python scripts used to automatically turn outdoor lighting on/off from a Raspberry Pi. Utilizes the Sunrise Sunset REST API to return times in JSON (https://sunrise-sunset.org/). Updated code pulls a better formatted JSON file which includes the date and insists the Pi operate in UTC mode.
<br>
<br>
Uses the following packges:<br>
python 3<br>
pip3<br>
python-requests<br>
python-dateutil<br>
<br>
Using the following cron to run this script at 2 am everyday and on system reboot (crontab -e):<br>
0 2 * * * /home/pi/OutdoorLighting/OutdoorLighting.py<br>
@reboot /home/pi/OutdoorLighting/OutdoorLighting.py<br>
