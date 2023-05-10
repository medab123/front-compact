
from time import sleep
import network # allow us to connet esp32 or esp8266 to a wifi network

     # garbage collector

import gc
gc.collect()
print(gc.mem_free())

ssid = 'AP EV'    
password = 'fiwi##2015'

station = network.WLAN(network.STA_IF)    # WiFi station
if station.active() == False:
    print('turning on interface wlan ....')
    station.active(True)
print('conecting to ',ssid,' ....')
station.connect(ssid, password)     # connect out esp board to our router

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())
#import webrepl
#webrepl.start(password="1234")












