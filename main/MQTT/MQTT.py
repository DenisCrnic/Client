import time
from main.MQTT.umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

class MQTT:
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.client_id = ubinascii.hexlify(machine.unique_id())
        self.client = MQTTClient(self.client_id, self.server_ip)
        self.msg = ""
        self.topic = ""
        try:
            self.connect()
        except OSError as e:
            self.restart_and_reconnect()
        

    def connect(self):
        self.client.set_callback(self.sub_cb)
        self.client.connect()
        print('Connected to %s MQTT broker' % (self.server_ip))
        return self.client
    
    def subscribe(self, topic):
        self.client.subscribe(topic)

    def sub_cb(self, topic, message):
        self.topic, self.msg = topic, message

    def restart_and_reconnect(self):
        print('Failed to connect to MQTT broker. Reconnecting...')
        time.sleep(5)
        machine.reset()

    def check_message(self):
        self.client.check_msg()
        