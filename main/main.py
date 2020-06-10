
import time
from main.MQTT import MQTT
from main.WiFi import WiFi

# WiFi Credentials
ssid = 'Denis'
password = 'ljubljana'

print("Trying to connect to wifi")
wifi = WiFi.WiFi(ssid, password)
print("Trying to connect to wifi 2")
wifi.initialization()

def start():  
  print("Trying to connect to MQTT 1")
  dht = MQTT.MQTT("192.168.1.150")
  print("Trying to connect to MQTT 2")

  dht.subscribe("request")

  while True:
    print("jaz sem izpis brez pomena")
    time.sleep(10)

def on_message(topic, message):
  print("Message arrived")
  print(topic, message)