from abc import ABC, abstractmethod
import time
import logging
import serial
import serial.tools.list_ports


class NeopyxelBackend(ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def add_stripe(self, NUMPIXELS, PIN):
        pass

    @abstractmethod
    def flush_stripes(self):
        pass

    @abstractmethod
    def set_pixel_color(self, stripe_number, pixel_number, color):
        pass

    @abstractmethod
    def show(self, stripe_number):
        pass


class ArduinoRelayBackend(NeopyxelBackend):
    def __init__(self, serial_port=None):
        super().__init__()
        comports = list(serial.tools.list_ports.comports())
        if serial_port is None:
            for comport in comports:
                if comport.pid is not None:
                    serial_port = comport.device
        self.__serial_port = serial_port
        self.__conn = serial.Serial(self.__serial_port, 28800, writeTimeout=0)
        time.sleep(1.8)

    def add_stripe(self, NUMPIXELS, PIN):
        cmd = bytearray(4)
        cmd[0] = 0
        cmd[1] = 3
        cmd[2] = NUMPIXELS
        cmd[3] = PIN
        self.__conn.write(cmd)
        logging.debug('ADD_STRIPE command sent: %s %s' %
                      (str(cmd[:2].hex()), str(cmd[2:].hex())))

    def flush_stripes(self):
        cmd = bytearray(2)
        cmd[0] = 0
        cmd[1] = 4
        self.__conn.write(cmd)
        logging.debug('FLUSH command sent: %s' % (str(cmd.hex())))

    def set_pixel_color(self, stripe_number, pixel_number, color):
        cmd = bytearray(6)
        cmd[0] = stripe_number
        # Set Pixel Color Command decode
        cmd[1] = 1
        cmd[2] = pixel_number
        cmd[3] = color[0]
        cmd[4] = color[1]
        cmd[5] = color[2]
        self.__conn.write(cmd)
        logging.debug('SET_PIXEL_COLOR command sent: %s %s' %
                      (str(cmd[:3].hex()), str(cmd[3:].hex())))
        while self.__conn.out_waiting > 0:
            continue  # waiting for command to be read

    def show(self, stripe_number):
        cmd = bytearray(2)
        cmd[0] = stripe_number
        cmd[1] = 2  # Show Command code
        self.__conn.write(cmd)
        time.sleep(0.01)
        logging.debug('SHOW command sent: %s' % (str(cmd.hex())))

    def __del__(self):
        self.__conn.close()


# class RaspberryPiBackend(NeopyxelBackend):
