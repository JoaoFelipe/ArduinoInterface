ArduinoInterface
================

## Embedded Computing System project - laptop 

Language: jython

This program executes 5 different threads in order to establish the communication between the android and the arduino:
- RoughMovementThread: Keep sending requests to the website to check if the android app detected a rough movement. If rough movement detected, sends to arduino
- ReallyRoughMovementThread: The same thing, but for really rough movement
- LightSwitchThread: Keep sending requests to the website to check the light status and when it changes
- ArduinoListener: Reads the serial data to collect light change status and heart-rate status and sends to website
- BluetoothWaitThread: Creates a bluetooth server to establish a direct connection between this program and the android device via bluetooth and get the data faster, by not requiring to do requests to the website 

Dependencies:

1.  Python:
	- PySerial: https://pypi.python.org/pypi/pyserial
		* Establish the Serial connection with arduino
		* Install by using jython setup.py install
1.  Java:
	- Bluecove: http://bluecove.org/
		* Java library for Bluetooth
		* Install by creating a <name>.pth file at jython/lib/site-packages and writing the path to bluecove jar file
	- RXTX: http://users.frii.com/jarvi/rxtx/
		* Java library for serial connection (used by PySerial)
		* Install on ubuntu: run sudo apt-get install librxtx-java
		* Create a <name>.pth file at jython/lib/site-packages with the following paths:
			+ /usr/share/java/RXTXcomm.jar
			+ /usr/share/java/RXTXcomm-2.2pre2.jar
		
Running:
- jython main.py

Collaborators:
- Tiago Pimentel Martins da Silva - t.pimentelms@gmail.com
- Joao Felipe Nicolaci Pimentel	- joaofelipenp@gmail.comy
- Matheus Fernandes de Camargo	- matheusfc09@gmail.com
