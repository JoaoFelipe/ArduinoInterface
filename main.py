from java.lang import Thread as JThread
from Arduino import Arduino

if __name__=='__main__':
    wait_thread = JThread(Arduino())
    wait_thread.start()
    
    