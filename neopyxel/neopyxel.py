import time
import serial
import serial.tools.list_ports

class NeopixelStripe:
    def __init__(self, NUMPIXELS, serial_port = 'COM5'):
        self.NUMPIXELS = NUMPIXELS
        comports = list(serial.tools.list_ports.comports())
        for comport in comports:
            if comport.pid != None:
                serial_port = comport.device
        self.serial_port = serial_port
        self.conn = serial.Serial(self.serial_port, 28800, writeTimeout = 0)
        time.sleep(1.8)

    def setPixelColor(self, stripe_number, pixel_number, color):
        cmd = bytearray(6)
        cmd[0] = stripe_number
        cmd[1] = 1 # Set Pixel Color Command decode
        cmd[2] = pixel_number
        cmd[3] = color[0]
        cmd[4] = color[1]
        cmd[5] = color[2]
        self.conn.write(cmd)

    def show(self, stripe_number):
        cmd = bytearray(2)
        cmd[0] = stripe_number
        cmd[1] = 2 # Show Command code
        self.conn.write(cmd)

    def __del__(self):
        self.conn.close()
