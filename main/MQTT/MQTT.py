import time
import utime
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
from main.LED_indicator import LED_indicator
import logging



timer = machine.Timer(0)

# Če se 10x poskušamo reconectat na broker, vrže recursion error.
#  

class MQTT:
    # Passed arg: server ip, main object with callback function
    def __init__(self, server_ip, main, CLIENT_ROOT_TOPIC):
        self.main = main # Main function object (main/main.py Class), so we can make a call to on_message function
        # Logging initialisation
        self.MQTT_STATE_TOPIC = CLIENT_ROOT_TOPIC + '/ping'
        self.MQTT_REQUEST_TOPIC = CLIENT_ROOT_TOPIC + b'/request'
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger(__file__)

        self.number_of_fails = 0
        self.max_number_of_fails = 10

        self.server_ip = server_ip
        self.client_id = ubinascii.hexlify(machine.unique_id())
        self.led = LED_indicator.LED_indicator(4, 0)
        self.led.set_state(3)
        self.mqtt_state = False
        self.connect()
        #timer.init(period=10000, mode=machine.Timer.PERIODIC, callback=self.send_state)
        _thread.start_new_thread(self.check_message, ())
    

    def connect(self):
        try:
            self.log.info("0")
            self.client = MQTTClient(self.client_id, self.server_ip, keepalive=15)
            self.log.info("1")
            self.client.set_last_will(self.MQTT_STATE_TOPIC, '0', retain=True)
            self.log.info("2")
            self.client.set_callback(self.sub_cb)
            self.log.info("3")
            self.client.connect()
            self.log.info("4")
            self.client.subscribe(self.MQTT_REQUEST_TOPIC)
            self.log.info("5")
            self.client.subscribe(self.MQTT_STATE_TOPIC)
            self.log.info("6")
            self.client.publish(self.MQTT_STATE_TOPIC, '1')
            self.log.info("7")
            self.last_message_time = utime.ticks_ms()
            self.log.info("8")
            self.log.info('Connected to %s MQTT broker', (self.server_ip))
            self.mqtt_state = True
            self.log.info("9")
            self.led.set_state(1)
            self.log.info("10")

        except OSError as e:
            self.log.error("Couldn't connect to MQTT broker, retrying ... ")
            return

    def reconnect(self):
        # isto kot while not self.mqtt_state, le da kličemo dodatno funkcijo
        # da lahko upravjamo z indentifikacijsko led diodo
        while not self.isConnected():
            # time.sleep(2)
            self.connect()

    def sub_cb(self, topic, message):
        self.log.info("%s %s", topic, message)
        # Remember time of last message for conn check
        self.last_message_time = utime.ticks_ms()
        # self.log.info(utime.ticks_ms())
        self.main.on_message(topic, message)

    def pub(self, topic, msg):
        self.client.publish(topic, msg)

    def ping(self):
        self.pub(self.MQTT_STATE_TOPIC, "1")

    def get_request_topic(self):
        return self.MQTT_REQUEST_TOPIC

    def isConnected(self):
        if self.mqtt_state:
            self.led.set_state(1)
            self.log.info("Server connection ... OK")
            return True

        else:
            self.led.set_state(2)
            self.log.error("No connection to the server")
            return False
        

    def check_message(self):
        TIMEOUT = 10 * 1000 # _s * 1000 to get miliseconds!!!
        while True:
            time.sleep(0.2)
            #self.log.info("Inside check message")
            try:
                # Preglej če je v zadnjih $TIMEOUT sec prispelo katerokoli sporocilo
                #self.log.info(utime.ticks_ms() - self.last_message_time < TIMEOUT) 
                if (utime.ticks_ms() - self.last_message_time < TIMEOUT): # ta čas ne sme biti daljši od keep alive tima (v funkciji __init__())
                    #self.log.info("Sporocilo je prispelo v zadnjih %d sec", TIMEOUT/1000)
                    self.number_of_fails = 0
                    # Če ja, potem poslušaj naprej ter ponovi vse skupaj
                    self.client.check_msg()
                
                else:
                    self.log.info("Sporocilo NI prispelo!!!!!!!")
                    # Če že 20 sec ni bilo sporočila, pingni, ter poslušaj odgovor
                    self.number_of_fails += 1
                    # nmesto pinga ustvari ping topic
                    self.log.error("ping 1")
                    self.ping()
                    self.log.error("ping 2")
                    time.sleep(0.2)
                    while self.client.check_msg():
                        self.log.error("ping 3")
                        # pass

                    # Ko dovoljkrat ne dobimo odgovora na ping pomeni da se je server sesul
                    
                    if self.number_of_fails == self.max_number_of_fails:
                        self.log.error("Katastrofa, server se je sesul")
                        self.mqtt_state = False
                        raise Exception("Server not responding")

            except Exception as err:
                self.log.error("Exception: %s", err)
                self.mqtt_state = False
                self.reconnect()


    # def send_state(self, timer):
    #     try:
    #         self.client.publish(MQTT_STATE_TOPIC, '1')
    #     except OSError as err:
    #         self.mqtt_state = False
    #         self.log.error("OS error: %s", err)
