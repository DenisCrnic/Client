from main import ota_updater

import network
import time

# from main.WiFi import WiFi
from main.WiFi import WiFi

from main.MQTT import MQTT

# WiFi Credentials
ssid = 'Denis'
password = 'ljubljana'

print("Trying to connect to wifi")
wifi = WiFi.WiFi(ssid, password)
print("Trying to connect to wifi 2")
wifi.initialisation()

print("Trying to connect to MQTT 1")
dht = MQTT.MQTT("192.168.1.150")
print("Trying to connect to MQTT 2")

dht.subscribe("request")


def hello():

  while True:
      try:
        dht.check_message()
        print(dht.msg)
        time.sleep(2)
      except OSError as e:
        dht.restart_and_reconnect()
