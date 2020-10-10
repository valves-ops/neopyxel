import time
import itertools
from collections.abc import Iterable
import serial
import serial.tools.list_ports

class NeopyxelRelay():
    def __init__(self, serial_port=None):
        comports = list(serial.tools.list_ports.comports())
        if serial_port is None:
            for comport in comports:
                if comport.pid is not None:
                    serial_port = comport.device
        self.__serial_port = serial_port
        self.__conn = serial.Serial(self.__serial_port, 28800, writeTimeout=0)
        time.sleep(1.8)
        self.__stripes = []

    @property
    def stripes(self):
        return self.__stripes

    def add_stripe(self, NUMPIXELS, PIN):
        self.__stripes.append(Stripe(NUMPIXELS, PIN, self.__conn))
        cmd = bytearray(4)
        cmd[0] = 0
        cmd[1] = 3
        cmd[2] = NUMPIXELS
        cmd[3] = PIN
        self.__conn.write(cmd)

    def set_pixel_color(self, pixel_number, color):
        if isinstance(pixel_number, Iterable):
            for pixel in pixel_number:
                self.set_pixel_color(pixel, color)
        else:
            for stripe in self.__stripes:
                stripe.set_pixel_color(pixel_number, color)

    def show(self):
        for stripe in self.__stripes:
            stripe.show()

    def flush_stripes(self):
        cmd = bytearray(4)
        cmd[0] = 0
        cmd[1] = 4
        self.__conn.write(cmd)

    def __del__(self):
        self.flush_stripes()
        self.__conn.close()


class Stripe:
    counter = itertools.count()

    def __init__(self, NUMPIXELS, PIN, conn):
        self.__NUMPIXELS = NUMPIXELS
        self.__pixels = [VirtualPixel()]*self.__NUMPIXELS
        self.__PIN = PIN
        self.__stripe_number = next(Stripe.counter)
        self.__conn = conn

    @property
    def pixels(self):
        return self.__pixels

    @property
    def stripe_number(self):
        return self.__stripe_number
    
    @property
    def num_pixels(self):
        return self.__NUMPIXELS

    @property
    def pin(self):
        return self.__PIN

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
            self.__conn.write(cmd)
            self.__pixels[pixel_number].set_pixel_color(color)
            time.sleep(0.01)

    def show(self):
        cmd = bytearray(2)
        cmd[0] = self.stripe_number
        cmd[1] = 2  # Show Command code
        self.__conn.write(cmd)
        for pixel in self.pixels:
            pixel.show()


class VirtualPixel:
    def __init__(self, color=(0, 0, 0)):
        self.__displayed_color = color
        self.__buffer_color = color
        self.__coherent = True

    def set_pixel_color(self, color):
        self.__buffer_color = color
        if self.__buffer_color != self.__displayed_color:
            self.__coherent = False

    def show(self):
        if not self.__coherent:
            self.__displayed_color = self.__buffer_color
            self.__coherent = True

    def __str__(self):
        return '({}, {}, {})'.format(*self.__displayed_color)
