import time
import serial
import serial.tools.list_ports
import itertools
from collections.abc import Iterable


class NeopyxelRelay():
    def __init__(self, serial_port=None):
        comports = list(serial.tools.list_ports.comports())
        if serial_port is None:
            for comport in comports:
                if comport.pid is not None:
                    serial_port = comport.device
        self.serial_port = serial_port
        self.conn = serial.Serial(self.serial_port, 28800, writeTimeout=0)
        time.sleep(1.8)
        self._stripes = []

    def add_stripe(self, NUMPIXELS, PIN):
        self._stripes.append(Stripe(NUMPIXELS, PIN, self.conn))
        cmd = bytearray(4)
        cmd[0] = 0
        cmd[1] = 3
        cmd[2] = NUMPIXELS
        cmd[3] = PIN
        self.conn.write(cmd)

    def set_pixel_color(self, pixel_number, color):
        if isinstance(pixel_number, Iterable):
            for pixel in pixel_number:
                self.set_pixel_color(pixel, color)
        else:
            for stripe in self._stripes:
                stripe.set_pixel_color(pixel_number, color)

    def show(self):
        for stripe in self._stripes:
            stripe.show()

    def clear_stripes(self):
        cmd = bytearray(4)
        cmd[0] = 0
        cmd[1] = 4
        self.conn.write(cmd)

    def __del__(self):
        self.clear_stripes()
        self.conn.close()


class Stripe:
    counter = itertools.count()

    def __init__(self, NUMPIXELS, PIN, conn):
        self.NUMPIXELS = NUMPIXELS
        self.PIN = PIN
        self.stripe_number = next(Stripe.counter)
        self.conn = conn

    def set_pixel_color(self, pixel_number, color):
        if isinstance(pixel_number, Iterable):
            for pixel in pixel_number:
                self.set_pixel_color(pixel, color)
        else:
            cmd = bytearray(6)
            cmd[0] = self.stripe_number
            # Set Pixel Color Command decode
            cmd[1] = 1
            cmd[2] = pixel_number
            cmd[3] = color[0]
            cmd[4] = color[1]
            cmd[5] = color[2]
            self.conn.write(cmd)
            time.sleep(0.01)

    def show(self):
        cmd = bytearray(2)
        cmd[0] = self.stripe_number
        cmd[1] = 2  # Show Command code
        self.conn.write(cmd)
