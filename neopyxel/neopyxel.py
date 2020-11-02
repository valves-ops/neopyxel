import time
import itertools
from collections.abc import Iterable
import serial
import serial.tools.list_ports
import logging


class NeopyxelRelay():
    def __init__(self, serial_port=None, debug=False):
        if debug:
            level = logging.DEBUG
        else:
            level = logging.CRITICAL
        logging.basicConfig(format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=level)
        logging.debug('NEOPYXEL DEBUG MODE ON')
        comports = list(serial.tools.list_ports.comports())
        if serial_port is None:
            for comport in comports:
                if comport.pid is not None:
                    serial_port = comport.device
        self.__serial_port = serial_port
        self.__conn = serial.Serial(self.__serial_port, 28800, writeTimeout=0)
        time.sleep(1.8)
        self.__stripes = []
        self.__current_effect = None

    @property
    def stripes(self):
        return self.__stripes

    @property
    def conn(self):
        return self.__conn

    def add_stripe(self, NUMPIXELS, PIN):
        self.__stripes.append(Stripe(NUMPIXELS, PIN, self.__conn))
        cmd = bytearray(4)
        cmd[0] = 0
        cmd[1] = 3
        cmd[2] = NUMPIXELS
        cmd[3] = PIN
        self.__conn.write(cmd)
        logging.debug('ADD_STRIPE command sent: %s %s' %
                      (str(cmd[:2].hex()), str(cmd[2:].hex())))

    def set_pixel_color(self, pixel_number, color):
        for stripe in self.__stripes:
            stripe.set_pixel_color(pixel_number, color)

    def set_segment_color(self, segment_position, segment_length, color):
        for stripe in self.stripes:
            stripe.set_segment_color(segment_position, segment_length, color)

    def show(self):
        for stripe in self.__stripes:
            stripe.show()

    def execute_effect(self, EffectClass, **kwargs):
        if self.__current_effect is not None:
            self.__current_effect.stop()
        self.__current_effect = EffectClass(self, **kwargs)
        self.__current_effect.start()

    def stop_effect(self):
        if self.__current_effect is not None:
            self.__current_effect.stop()

    def flush_stripes(self):
        cmd = bytearray(2)
        cmd[0] = 0
        cmd[1] = 4
        self.__conn.write(cmd)
        logging.debug('FLUSH command sent: %s' % (str(cmd.hex())))

    def __del__(self):
        self.flush_stripes()
        self.__conn.close()


class Stripe:
    counter = itertools.count()

    def __init__(self, NUMPIXELS, PIN, conn):
        self.__NUMPIXELS = NUMPIXELS
        self.__pixels = [VirtualPixel() for i in range(self.__NUMPIXELS)]
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
            if self.__pixels[pixel_number].buffer_color != color:
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
                logging.debug('SET_PIXEL_COLOR command sent: %s %s' %
                              (str(cmd[:3].hex()), str(cmd[3:].hex())))
                while self.__conn.out_waiting > 0:
                    continue  # waiting for command to be read

    def set_segment_color(self, segment_position, segment_length, color):
        pixel_start = self.__get_start_pixel(segment_position)
        num_pixels = self.__get_length_in_pixels(segment_length)
        num_pixels = min(pixel_start+num_pixels, self.__NUMPIXELS)
        pixels = list(range(pixel_start, num_pixels))
        self.set_pixel_color(pixels, color)

    def __get_start_pixel(self, segment_position):
        position = round(self.__NUMPIXELS*segment_position)
        position = min(position, self.__NUMPIXELS-1)
        position = max(position, 0)
        return position

    def __get_length_in_pixels(self, segment_length):
        length = round(self.__NUMPIXELS*segment_length)
        length = min(length, self.__NUMPIXELS)
        length = max(length, 1)
        return length

    def show(self):
        pixels_coherent = all([pixel.is_coherent for pixel in self.pixels])
        if not pixels_coherent:
            cmd = bytearray(2)
            cmd[0] = self.stripe_number
            cmd[1] = 2  # Show Command code
            self.__conn.write(cmd)
            for pixel in self.pixels:
                pixel.show()
            time.sleep(0.01)
            logging.debug('SHOW command sent: %s' % (str(cmd.hex())))


class VirtualPixel:
    def __init__(self, color=(0, 0, 0)):
        self.__displayed_color = color
        self.__buffer_color = color
        self.__coherent = True

    @property
    def is_coherent(self):
        return self.__coherent

    @property
    def displayed_color(self):
        return self.__displayed_color

    @property
    def buffer_color(self):
        return self.__buffer_color

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
