from java.lang import Thread as JThread
from java.lang import Runnable
from javax.bluetooth import DiscoveryAgent, LocalDevice, UUID
from javax.microedition.io import Connector
from ProcessConnectionThread import ProcessConnectionThread

class BluetoothWaitThread(Runnable):
    
    def __init__(self, arduino):
        self.arduino = arduino
    
    def run(self):
        self.wait_for_connection()
        
    def wait_for_connection(self):
        local = None
        notifier = None
        connection = None
        try:
            local = LocalDevice.getLocalDevice()
            local.setDiscoverable(DiscoveryAgent.GIAC)
            uuid = UUID(80087355) # "04c6093b-0000-1000-8000-00805f9b34fb"
            url = "btspp://localhost:" + uuid.toString() + ";name=RemoteBluetooth";
            notifier = Connector.open(url);
        except Exception:
            print "Bluetooth Device is not available"
            return
        
        while True:
            try:
                print "waiting for connection..."
                connection = notifier.acceptAndOpen();
                processThread = JThread(ProcessConnectionThread(connection, self.arduino));
                processThread.start()
            except Exception:
                print "Bluetooth Device is not available"
                return
        