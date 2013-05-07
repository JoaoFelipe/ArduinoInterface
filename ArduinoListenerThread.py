"""    ArduinoListenerThread.py
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
    Listen to arduino commands and realize a post request if the arduino says to turn the lights on of off

"""

from java.lang import Runnable

class ArduinoListenerThread(Runnable):
    
    def __init__(self, arduino):
        self.arduino = arduino
        
    def run(self):
        while True:
            if not self.arduino.arduino:
                continue
            line = self.arduino.arduino.readline()
            print line
            with open("log.txt", "a") as myfile:
                myfile.write(self.arduino.get_time() + ' ' + line + '\n')
            
            if 'DATA 0' in line:
                self.arduino.switch_lights(0)
            elif 'DATA 1' in line:
                self.arduino.switch_lights(1)
            elif 'DATA 2' in line:
                self.arduino.send_heart_rate(line.split(' ')[-1])
                
