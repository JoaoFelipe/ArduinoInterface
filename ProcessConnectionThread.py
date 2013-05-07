"""    ProcessConnectionThread.py
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
    Process the bluetooth connection
    
 Version log:
    30/04/2013 Joao Felipe
        Sending light status through bluetooth

"""

from java.lang import Runnable
from java.nio import ByteBuffer

EXIT_CMD = -1
START = 2
END = 3
SET_LIGHT_STATUS = 76
REQUEST_LIGHT_STATUS = 82
SET_ROUGH = 109
SET_REALLY_ROUGH = 77

class ProcessConnectionThread(Runnable):

    def __init__(self, connection, arduino):
        self.connection = connection
        self.arduino = arduino
        self.buffer = []
        self.count = 0;
        self.first = False
        
    def run(self):
        try:
            input_stream = self.connection.openInputStream()
            self.output_stream = self.connection.openOutputStream()
            print "waiting for input"
            while True:
                command = input_stream.read()
                if command == EXIT_CMD:
                    print "finish process"
                    break
                self.process_command(command)
        except Exception:
            print "Bluetooth Device is not available"
    
    def process_command(self, command):
        if command == START and self.count <= 0:
            self.buffer = []
            self.first = True
        elif command == END and self.count <= 0:
            print self.buffer
            buffer = ByteBuffer.allocate(len(self.buffer))
            for b in self.buffer:
                buffer.put(b)
            buffer.flip()
            cmd = buffer.get()
            if cmd == REQUEST_LIGHT_STATUS:
                self.send_light_status()
                pass
            elif cmd == SET_LIGHT_STATUS:
                time = buffer.getLong()
                status = buffer.get()
                print status    
                self.arduino.switch_arduino_lights(status, time)
            elif cmd == SET_ROUGH:
                time = buffer.getLong()
                self.arduino.send_rough_data(time)
            elif cmd == SET_REALLY_ROUGH:
                time = buffer.getLong()
                self.arduino.send_really_rough_data(time)
        else:
            self.buffer.append(command)
            if self.first:
                if command == SET_LIGHT_STATUS:
                    self.count = 10
                elif command == REQUEST_LIGHT_STATUS:
                    self.count = 1
                elif command == SET_ROUGH:
                    self.count = 9
                elif command == SET_REALLY_ROUGH:
                    self.count = 9
                self.first = False
        self.count -= 1

    def send_light_status(self):
        buffer = ByteBuffer.allocate(12)
        buffer.put(START)
        buffer.put(SET_LIGHT_STATUS)
        buffer.putLong(self.arduino.light_time)
        buffer.put(1 if self.arduino.light_status else 0)
        buffer.put(END)
        buf = buffer.array();
        self.output_stream.write(buf)
