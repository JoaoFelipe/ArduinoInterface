"""    LightSwitchThread.py
 Purpose: Final demo
 Author: Tiago Pimentel
        t.pimentelms@gmail.com
         Joao Felipe
        joaofelipenp@gmail.com
         Matheus Camargo
        matheusfc09@gmail.com
 CSE 467 -- Embedded Computing Systems
 WUSTL, Spring 2013
 Date: Apr., 29, 2013

 Description:
    Checks if the light button was pressed and sends to arduino

"""

import httplib
import time
from java.lang import Runnable
from java.lang import Thread as JThread

LIGHT_POWER_TIME = 1000

class LightSwitchThread(Runnable):
    
    def __init__(self, arduino):
        self.arduino = arduino
        
    def run(self):
        while True:
            if self.arduino.block_light_switch:
                JThread.currentThread().sleep(LIGHT_POWER_TIME);
                continue
            connection = httplib.HTTPConnection("sleepingbeauty.herokuapp.com")
            connection.request("GET", "/light_power/last.txt")
            response = connection.getresponse()
            if response.status == 200:
                data = [int(x) for x in response.read().split(',')]
                if len(data) == 1:
                    data.append(int(time.time()*1000))
                print "weblight ", data
                self.arduino.switch_arduino_lights(*data)
            JThread.currentThread().sleep(LIGHT_POWER_TIME);
