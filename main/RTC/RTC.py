import machine
import logging
import _thread
import time
# Logging initialisation
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__file__)

# https://forum.micropython.org/viewtopic.php?t=2264
#The documentation is wrong. You should use the "datetime" method.
# Also, the tuple is actually (year, month, day, weekday, hour, minute, second, millisecond).
# CODE: SELECT ALL

# >>>import machine
# >>>rtc=machine.RTC()
# >>>rtc.datetime((2014, 5, 1, 0, 4, 13, 0, 0))
# >>>rtc.datetime()
# (2014, 5, 1, 0, 4, 13, 0, 0)

# -4s (20:05)
#

class RTC:
    def __init__(self):
        self.rtc = machine.RTC()
        self.rtc.init((2020, 9, 11, 5, 20, 4, 30, 0))
        log.info(self.rtc.datetime())
        _thread.start_new_thread(self.run, ())
    
    def run(self):
        while True:
            log.info(self.rtc.datetime())
            time.sleep(1)
    