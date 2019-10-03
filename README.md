# OutdoorLighting
Python scripts used to automatically turn outdoor lighting on/off from a Raspberry Pi.

Uses the following packges:
python 3
pip3
python-requests
python-dateutil

Using the following cron to run this script at 1 am everyday and on system reboot (crontab -e):
0 1 * * * /home/pi/OutdoorLighting/OutdoorLighting.py
@reboot /home/pi/OutdoorLighting/OutdoorLighting.py
