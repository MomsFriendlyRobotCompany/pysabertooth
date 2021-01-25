##
# Sabertooth.py: Class implementing packetized serial control of
#                Sabertooth 2x32 motor driver (Dimension Engineering).
#
# This code was adapted from MIT licensed
# Copyright 2015, Egan McComb
# copywrite 2017 Kevin J. Walchko
#
##

import serial
import logging
import time


class Sabertooth(object):
    """
    Sabertooth: A class to control a Sabertooth 2x60 using the packetized
                serial mode (DIP switches 1,2 low).

    https://www.dimensionengineering.com/datasheets/Sabertooth2x60.pdf
    """
    FORWARD_1 = 0x00
    REVERSE_1 = 0x01
    FORWARD_2 = 0x04
    REVERSE_2 = 0x05
    FORWARD_MIXED = 0x08
    REVERSE_MIXED = 0x09
    RIGHT_MIXED = 0x0A
    LEFT_MIXED = 0x0B
    RAMP = 0x10

    def __init__(self, port, baudrate=9600, address=128, timeout=0.1):
        """
        baudrate - 2400, 9600, 19200, 38400, 115200
        address - motor controller address
        timeout - serial read time out
        """
        self.port = port
        self.address = address

        if 128 > self.address > 135:
            raise Exception('PySabertooth, invalid address: {}'.format(address))

        # if baudrate in [9600, 19200, 38400, 115200]:
        #     pass
        # else:
        #     raise Exception('PySabertooth, invalid baudrate {}'.format(baudrate))

        # Initialize serial port.
        self.saber = serial.Serial()
        self.saber.baudrate = baudrate
        self.saber.port = port
        self.saber.timeout = timeout

        self.open()
        self.setBaudrate(baudrate)

    def __del__(self):
        """
        Destructor, stops motors and closes serial port
        """
        self.stop()
        self.close()
        return

    def info(self):
        """
        Prints out connection info
        """
        print('')
        print('='*40)
        print('Sabertooth Motor Controller')
        print('  port: {}'.format(self.saber.port))
        print('  baudrate: {}  bps'.format(self.saber.baudrate))
        print('  address: {}'.format(self.address))
        print('-'*40)
        print('')

    def close(self):
        """
        Closes serial port
        """
        self.saber.close()

    def setBaudrate(self, baudrate):
        """
        Sets the baudrate to: 2400, 9600, 19200, 38400, 115200
        """
        valid = {
            2400:   1,
            9600:   2,
            19200:  3,
            38400:  4,
            115200: 5
        }

        if baudrate in valid:
            baud = valid[baudrate]
        else:
            raise Exception('PySabertooth, invalid baudrate {}'.format(baudrate))

        # command = 15
        # checksum = (self.address + command + baudrate) & 127
        self.sendCommand(15, baud)
        self.saber.write(b'\xaa')
        time.sleep(0.2)

    def open(self):
        """
        Opens serial port
        """
        if not self.saber.is_open:
            self.saber.open()
        self.saber.write(b'\xaa')
        self.saber.write(b'\xaa')
        time.sleep(0.2)

    def sendCommand(self, command, message):
        """
        sendCommand: Sends a packetized serial command to the Sabertooth

            command: Command to send.
                FORWARD_1 = 0x00
                REVERSE_1 = 0x01
                FORWARD_2 = 0x04
                REVERSE_2 = 0x05
                FORWARD_MIXED = 0x08
                REVERSE_MIXED = 0x09
                RIGHT_MIXED = 0x0A
                LEFT_MIXED = 0x0B
                RAMP = 0x10
            message: Command

        """
        # Calculate checksum termination (page 23 of the documentation).
        checksum = (self.address + command + message) & 127
        # Write data packet.
        msg = [self.address, command, message, checksum]
        msg = bytes(bytearray(msg))
        self.saber.write(msg)
        # Flush UART.
        self.saber.flush()

    def stop(self):
        """
        Stops both motors
        """
        sentBytes = 0
        self.driveBoth(0,0)
        return sentBytes

    def drive(self, num, speed):
        """Drive 1 or 2 motor"""
        # reverse commands are equal to forward+1
        cmds = [self.FORWARD_1, self.FORWARD_2]

        try:
            cmd = cmds[num-1]
        except:
            raise Exception('PySabertooth, invalid motor number: {}'.format(num))

        if speed < 0:
            speed = -speed
            cmd += 1

        if speed > 100:
            raise Exception('PySabertooth, invalid speed: {}'.format(speed))

        self.sendCommand(cmd, int(127*speed/100))

    def driveBoth(self, speed1, speed2):
        """Drive both 1 and 2 motors at once"""
        self.drive(1, speed1)
        self.drive(2, speed2)

    def text(self, cmds):
        """Send the simple ASCII commands"""
        self.saber.write(cmds + b'\r\n')

    def textGet(self, cmds):
        """Send the simple ASCII commands"""
        self.text(cmds)
        ans = self.saber.read(100)
        return ans
