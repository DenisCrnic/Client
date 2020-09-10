from time import sleep
import network
from main.LED_indicator import LED_indicator
import _thread
#from main.WiFi import slimDNS

class WiFi:
    def __init__(self, ssid, passwd):
        self.ssid = ssid
        self.passwd = passwd
        self.station = network.WLAN(network.STA_IF)
        # Led indicator for wifi initialization
        self.led = LED_indicator.LED_indicator(17, 16)

        # Start a new thread for checking wifi conn
        _thread.start_new_thread(self.run, ())

        # Sfaljen mDDNS poskus
        #self.DNSserver = slimDNS.SlimDNSServer(self.station.ifconfig()[0], "esp32")
        #_thread.start_new_thread(self.DNSserver.run_forever(), ())
        
     
    def initialization(self):
        try:
            self.station.active(True)
            self.station.connect(self.ssid, self.passwd)
        except OSError as e:
            print("WiFi error:", e)
            self.led.set_state(2)

        print("Connecting to wifi")
        while self.station.isconnected() == False:
            self.led.set_state(3)
            #pass
        
        self.led.set_state(1)
        print('Connection successful')
        print(self.station.ifconfig())

    def run(self):
        while True:
            if self.station.isconnected():
                self.led.set_state(1)
            else:
                self.led.set_state(2)
            sleep(0.2)

    def get_IP(self):
        return self.station.ifconfig()[0]