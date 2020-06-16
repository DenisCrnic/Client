
import time
from main import ota_updater
from main.MQTT import MQTT
from main.WiFi import WiFi
from main.Web import Web
import ujson
import logging
from machine import ADC, Pin

class Main:
  def __init__(self):
    # Input sensors
    self._pins = (36, 39, 34)
    self.topics = ('SECCS/client/load_1', 'SECCS/client/load_2', 'SECCS/client/load_3')
    self.CLIENT_root_topic = b'SECCS/client'
    self.input_devices = [ADC(Pin(x)) for x in self._pins]

    # Nastavi branje 0 - 3.6 V (default 0 - 1 V)
    for device in self.input_devices:
      device.atten(ADC.ATTN_11DB)

    # Logging initialisation
    logging.basicConfig(level=logging.INFO)
    self.log = logging.getLogger(__file__)

    # WiFi Credentials
    self.SSID = 'Denis'
    self.password = 'ljubljana'

    # MQTT variables
    self.MQTT_broker_IP = "192.168.1.150"

    # Connect to wifi
    self.wifi_connect()

  def wifi_connect(self):
    self.log.info("Trying to connect to wifi")
    # Create wifi object with proper credentials
    self.wifi = WiFi.WiFi(self.SSID, self.password)
    self.log.info("WiFi initialisation ... ")
    self.wifi.initialization()
    self.log.info("OK")

  def mqtt_connect(self):
    self.log.info("Trying to connect to MQTT ... ")
    self.mqtt = MQTT.MQTT(self.MQTT_broker_IP, self, self.CLIENT_root_topic)
    self.log.info("OK")

  def on_message(self, topic, message):
    # self.log.info("Message %s arrived on %s topic", message, topic)
    if topic == self.mqtt.get_request_topic():
      self.log.info("inside request")
      for device, topic in zip(self.input_devices, self.topics):
        
        msg = device.read()
        self.log.info("reading from device: %s", msg)
        self.mqtt.pub(topic, str(msg))
        self.log.info("published")

  def start(self):
    self.mqtt_connect()
    self.web = Web.Web("192.168.1.89") # Obtain any IP or hostname from wifi initialisation

main = Main()

def download_and_install_update_if_available():
    o = ota_updater.OTAUpdater('https://github.com/DenisCrnic/SECCS_client/')
    o.download_and_install_update_if_available()
    o.check_for_update_to_install_during_next_reboot()

print("Download and install update if available")
download_and_install_update_if_available()

main.start()