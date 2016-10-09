import serial
import teensy.serial_constants
import utils


class LightSender(object):

    def __init__(self,
            serial_port=teensy.serial_constants.SERIAL_ADDR,
            nlights=teensy.serial_constants.TOTAL_LEDS):

        self.nlights = nlights
        self.serial = serial.Serial(
                serial_port, teensy.serial_constants.BAUD, timeout=1)
        self.data = bytearray([0] * (self.nlights * 3))

    def strobe(self):
        i = 0
        strobe_cycle = 2
        while True:
            i += 1
            if i % strobe_cycle < strobe_cycle / 2:
                data = chr(100) * (self.nlights * 3)
            else:
                data = chr(0) * (self.nlights * 3)
            self.send_rgb(data.encode())

    def fetch_rgb(self):
        hex_colors, freq_staleness = self.get_hex_arr()
        for i, hex_color in enumerate(hex_colors):
            rgbtuple = utils.hex_to_rgb(hex_color)
            self.data[3 * i:3 * i + 3] = rgbtuple

    def send_rgb(self, data):
        self.serial.write(data)
        self.serial.flush()

    def update(self):
        while True:
            self.fetch_rgb()
            self.send_rgb(self.data)
