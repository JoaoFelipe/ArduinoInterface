import glob
import serial
import time
import urllib, urllib2
from java.lang import Runnable
from java.lang import Thread as JThread
from BluetoothWaitThread import BluetoothWaitThread
from LightSwitchThread import LightSwitchThread
from ReallyRoughMovementThread import ReallyRoughMovementThread
from RoughMovementThread import RoughMovementThread
from ArduinoListenerThread import ArduinoListenerThread

ARDUINO_RATE = 9600
START_TIME = 5000

class Arduino(Runnable):
    
    def __init__(self):
        self.arduino = None
        self.light_time = 0
        self.light_status = 0
        self.really_rough_time = 0
        self.rough_time = 0
        self.block_light_switch = False
    
    # connect_arduino
    # connect arduino to serial port
    def connect_arduino(self):
        usbs = glob.glob('/dev/ttyUSB*')
        if usbs:
            self.usb = usbs[0]
            self.arduino = serial.Serial(self.usb, ARDUINO_RATE)
            
    # serial_write
    # writes data to arduino serial port
    # receives string
    def serial_write(self, send):
        print "Serial write ", send
        if self.arduino:
            print send
            self.arduino.write(send.encode('ascii'))
        
    # get_time
    # get current timestamp
    # returns string
    def get_time(self):
        return str(int(time.time()))
        
    # send_really_rough_data
    # sends serial data to arduino about the really rough movements
    # receives 0 or 1 and the timestamp
    def send_rough_data(self, time):
        if self.rough_time >= time:
            return
        self.rough_time = time
        self.serial_write("Data1"+str(time)+"a")    
        
    # switch_arduino_lights
    # sends serial data to arduino to turn the lights on or off
    # receives 0 or 1 and the timestamp
    def switch_arduino_lights(self, on_off, time):
        if self.light_time >= time:
            return
        self.light_time = time
        self.light_status = on_off
        self.serial_write("Data2"+ str(1 if on_off else 0))
        
        
    # send_really_rough_data
    # sends serial data to arduino about the really rough movements
    # receives 0 or 1 and the timestamp
    def send_really_rough_data(self, time):
        if self.really_rough_time >= time:
            return
        self.really_rough_time = time
        self.serial_write("Data3"+str(time)+"a")
    
    # switch_lights
    # sends post request to turn the lights on or off
    # receives 0 or 1
    def switch_lights(self, on_off):
        self.block_light_switch = True
        self.light_time = int(time.time()*1000)
        self.light_status = on_off
        params = urllib.urlencode({
            'light_power[on]': str(self.light_status),
            'light_power[time]': str(self.light_time),
        })
        url = "http://sleepingbeauty.herokuapp.com/light_power"
        req = urllib2.Request(url, params)
        try:
            urllib2.urlopen(req)
        except urllib2.URLError:
            pass
        self.block_light_switch = False
        
    # send_heart_rate
    # sends post request to store the heart rates
    # receives heart rate in bpm
    def send_heart_rate(self, value):
        params = urllib.urlencode({
            'heart_rate[rate]': str(value),
            'heart_rate[time]': str(int(time.time()*1000)),
        })
        url = "http://sleepingbeauty.herokuapp.com/heart_rates"
        req = urllib2.Request(url, params)
        try:
            urllib2.urlopen(req)
        except urllib2.URLError:
            pass

    # run
    # execute threads
    def run(self):
        if not self.arduino:
            self.connect_arduino()
        JThread.currentThread().sleep(START_TIME);
        self.serial_write("Time"+self.get_time()+"a")
        threads = [
            JThread(RoughMovementThread(self)),
            JThread(ReallyRoughMovementThread(self)),
            JThread(LightSwitchThread(self)),
            JThread(ArduinoListenerThread(self)),
            JThread(BluetoothWaitThread(self)),
        ]
        for thread in threads:
            thread.start()