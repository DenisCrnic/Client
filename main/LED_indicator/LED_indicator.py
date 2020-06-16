from machine import ADC, Pin, PWM
from time import sleep
import _thread

class LED_indicator:
    def __init__(self, pin_r, pin_g):
        #initialize inputs
        self.pin_r = pin_r
        self.pin_g = pin_g
        self.led_r = Pin(pin_r, Pin.OUT)
        self.led_r.off()
        self.led_g = Pin(pin_g, Pin.OUT)
        self.led_g.off()
        self.state = 0

        _thread.start_new_thread(self.run, ())

    def run(self):
        while True:
            if self.state is 0:
                # all off
                
                self.led_r.off()
                self.led_g.off()
                sleep(0.2)

            elif self.state is 1:
                # heartbeat
                self.led_r.off()
                self.led_g.on()
                sleep(0.2)
                self.led_g.off()
                sleep(1.5)

            elif self.state is 2:
                # red blinking
                self.led_g.off()
                self.led_r.on()
                sleep(1)
                self.led_r.off()
                sleep(1)
        
            elif self.state is 3:
                # fast green blinking
                self.led_r.off()
                self.led_g.on()
                sleep(0.1)
                self.led_g.off()
                sleep(0.1)

    def set_state(self, st):
        self.state = st
            
