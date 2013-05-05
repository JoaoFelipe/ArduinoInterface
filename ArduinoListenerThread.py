from java.lang import Runnable

# ArduinoListenerThread
# Listen to arduino commands and realize a post request if the arduino says to turn the lights on of off
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
                