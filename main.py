"""    main.py
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
    This is the main of the interface with internet/bluetooth for android

"""

from java.lang import Thread as JThread
from Arduino import Arduino

if __name__=='__main__':
    wait_thread = JThread(Arduino())
    wait_thread.start()
    
    
