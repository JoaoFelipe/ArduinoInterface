"""    RoughMovementThread.py
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
    Checks if a rough movement occurred and sends to arduino

"""

import httplib
from java.lang import Runnable
from java.lang import Thread as JThread

ROUGH_TIME = 10000

class RoughMovementThread(Runnable):
    
    def __init__(self, arduino):
        self.arduino = arduino
    
    def run(self):
        while True:
            connection = httplib.HTTPConnection("sleepingbeauty.herokuapp.com")
            connection.request("GET", "/rough_movements/last_time.txt")
            response = connection.getresponse()
            if response.status == 200:
                self.arduino.send_rough_data(int(response.read()))
            JThread.currentThread().sleep(ROUGH_TIME);
