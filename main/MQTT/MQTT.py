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
import _thread
from main import main

class MQTT:
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.client_id = ubinascii.hexlify(machine.unique_id())
        self.client = MQTTClient(self.client_id, self.server_ip)
        try:
            self.connect()
        except OSError as e:
            self.restart_and_reconnect()
        _thread.start_new_thread(self.check_message, ())
        

    def connect(self):
        self.client.set_callback(self.sub_cb)
        self.client.connect()
        print('Connected to %s MQTT broker' % (self.server_ip))
        return self.client
    
    def subscribe(self, topic):
        self.client.subscribe(topic)

    def sub_cb(self, topic, message):
        print("to sikundo je prispelo sporocilo")
        main.on_message(topic, message)

    def restart_and_reconnect(self):
        print('Failed to connect to MQTT broker. Reconnecting...')
        time.sleep(10)
        machine.reset()

    def check_message(self):
        while True:
            self.client.check_msg()
            time.sleep(0.1)
        