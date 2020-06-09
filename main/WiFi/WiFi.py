import network

class WiFi:
    def __init__(self, ssid, passwd):
        self.ssid = ssid
        self.passwd = passwd
        self.station = network.WLAN(network.STA_IF)
        

    def initialisation(self):
        self.station.active(True)
        self.station.connect(self.ssid, self.passwd)

        while self.station.isconnected() == False:
            pass

        print('Connection successful')
        print(self.station.ifconfig())

    
    