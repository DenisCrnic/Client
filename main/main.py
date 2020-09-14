import time
from main import ota_updater
from main.MQTT import MQTT
from main.WiFi import WiFi
from main.Web import Web
from main.RTC import RTC
import ujson
import logging
from machine import ADC, Pin
import gc
import micropython

# Logging initialisation
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__file__)

class Main:
  def __init__(self):
    # Input sensors
    print('-----------------------------')
    print('Initial free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
    print('-----------------------------')
    self._pins = (36, 39, 34)
    self.topics = ('SECCS/client_2/load_1', 'SECCS/client_2/load_2', 'SECCS/client_2/load_3')
    self.CLIENT_root_topic = b'SECCS/client_2'
    self.input_devices = [ADC(Pin(x)) for x in self._pins]

    # Nastavi branje 0 - 3.6 V (default 0 - 1 V)
    for device in self.input_devices:
      device.atten(ADC.ATTN_11DB)

    # WiFi Credentials
    self.SSID = 'Denis'
    self.password = 'ljubljana'

    # MQTT variables
    self.MQTT_broker_IP = "192.168.1.150"

  def on_message(self, topic, message):
    # log.info("Message %s arrived on %s topic" % message, topic)
    if topic == self.mqtt.get_request_topic():
      for device, topic in zip(self.input_devices, self.topics):
        msg = device.read()
        log.info("Publishing from device: %s" % msg)
        self.mqtt.pub(topic, str(msg))
        log.info("OK")

  def start(self):
    print('-----------------------------')
    print('Initial free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
    print('-----------------------------')
    self.wifi = WiFi.WiFi(self.SSID, self.password)
    print('-----------------------------')
    print('Initial free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
    print('-----------------------------')
    self.rtc = RTC.RTC()
    print('-----------------------------')
    print('Initial free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
    print('-----------------------------')
    log.info("Download and install update if available")
    self.download_and_install_update_if_available()
    print('-----------------------------')
    print('Initial free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
    print('-----------------------------')
    self.mqtt = MQTT.MQTT(self.MQTT_broker_IP, self, self.CLIENT_root_topic)
    print('-----------------------------')
    print('Initial free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
    print('-----------------------------')
    self.web = Web.Web(self.wifi.get_IP()) # Obtain any IP or hostname from wifi initialisation
    print('-----------------------------')
    print('Initial free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
    print('-----------------------------')
    log.info("Program terminated (escaped the loop)")

  def download_and_install_update_if_available(self):
      o = ota_updater.OTAUpdater('https://github.com/DenisCrnic/SECCS_client')
      o.download_and_install_update_if_available()
      o.check_for_update_to_install_during_next_reboot()

main = Main()
main.start()