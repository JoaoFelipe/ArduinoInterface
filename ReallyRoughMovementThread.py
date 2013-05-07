"""    ReallyRoughMovementThread.py
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
    Checks if a really rough movement occurred and sends to arduino

"""

import httplib
from java.lang import Runnable
from java.lang import Thread as JThread

REALLY_ROUGH_TIME = 1000

class ReallyRoughMovementThread(Runnable):
    
    def __init__(self, arduino):
        self.arduino = arduino
        
    def run(self):
        while True:
            connection = httplib.HTTPConnection("sleepingbeauty.herokuapp.com")
            connection.request("GET", "/rough_movements/last_time.txt?really_rough=1")
            response = connection.getresponse()
            if response.status == 200:
                self.arduino.send_really_rough_data(int(response.read()))
            JThread.currentThread().sleep(REALLY_ROUGH_TIME);
            
