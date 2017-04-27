from time import sleep
import serial

class LightConnection:
	def __init__(self,dev,delay=.01,data_rate=9600):
		self.ser = serial.Serial(dev,data_rate)
		self.delay = delay

	def send_rgb_values(self,rgb_values):
		for i in rgb_values:
			self.ser.write(chr(i))

	def send_rgb_sequence(self,sequence):
		for rgb_values in sequence:
			self.send_rgb_values(rgb_values)
			sleep(self.delay)

ports=serial.tools.list_ports.comports()
p=ports[0]
# dev = '/dev/ttyACM2'
light_connection = LightConnection(p.device)

num_lights = 48
message = []
for j in range(127,0,-2):
	message.append([j,127-j,0]*num_lights)

light_connection.send_rgb_sequence(message)
