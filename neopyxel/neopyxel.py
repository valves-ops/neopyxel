import itertools
from collections.abc import Iterable
import logging


class NeopyxelRelay():
    def __init__(self, Backend, serial_port=None, debug=False):
        if debug:
            level = logging.DEBUG
        else:
            level = logging.CRITICAL
        logging.basicConfig(format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=level)
        logging.debug('NEOPYXEL DEBUG MODE ON')
        self.backend = Backend(serial_port)
        self.__stripes = []
        self.__current_effect = None

    @property
    def stripes(self):
        return self.__stripes

    def add_stripe(self, NUMPIXELS, PIN):
        self.stop_effect()
        self.__stripes.append(Stripe(NUMPIXELS, PIN, self.backend))
        self.backend.add_stripe(NUMPIXELS, PIN)

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
        self.stop_effect()
        self.backend.flush_stripes()
        self.__stripes = []

    def __del__(self):
        self.flush_stripes()
        del self.backend


class Stripe:
    counter = itertools.count()

    def __init__(self, NUMPIXELS, PIN, backend):
        self.__NUMPIXELS = NUMPIXELS
        self.__pixels = [VirtualPixel() for i in range(self.__NUMPIXELS)]
        self.__PIN = PIN
        self.__stripe_number = next(Stripe.counter)
        self.backend = backend

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
                self.backend.set_pixel_color(
                    self.stripe_number, pixel_number, color)
                self.__pixels[pixel_number].set_pixel_color(color)

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
            self.backend.show(self.stripe_number)
            for pixel in self.pixels:
                pixel.show()


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
