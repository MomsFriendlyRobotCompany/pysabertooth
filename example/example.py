#!/usr/bin/env python

from __future__ import print_function, division
from pysabertooth import Sabertooth
import time


port = '/dev/serial/by-id/usb-Dimension_Engineering_Sabertooth_2x32_16004F410010-if01'


def ascii():
	# saber = Sabertooth(port, baudrate=115200)
	saber = Sabertooth(port, baudrate=38400)

	try:
		print('temperature [C]: {}'.format(saber.textGet(b'm2:gett')))
		print('battery [mV]: {}'.format(saber.textGet(b'm2:getb')))
		saber.text(b'm1:startup')
		saber.text(b'm2:startup')
		for speed in range(-2000, 2000, 500):
			# print('.')
			# def independentDrive(self, dir_left="fwd", speed_left=0, dir_right="fwd", speed_right=0)
			# saber.independentDrive('fwd', 50, 'fwd', 50)
			saber.text(b'm1:{}'.format(speed))
			saber.text(b'm2:{}'.format(speed))

			# format returned text
			m1 = saber.textGet(b'p1:get').split()[1]
			m2 = saber.textGet(b'p2:get').split()[1]
			c1 = saber.textGet(b'm1:getc')[:-2].split('C')[1]
			c2 = saber.textGet(b'm2:getc')[:-2].split('C')[1]
			# print(c1)
			print('M1: {:6} {:>6} mA   M2: {:6} {:>6} mA'.format(m1, c1, m2, c2))
			time.sleep(1)

	except KeyboardInterrupt:
		print('keyboard interrupt ... ')


	saber.text(b'm1:0')
	saber.text(b'm2:0')
	time.sleep(0.1)
	saber.stop()


def packet():
	# saber = Sabertooth(port, baudrate=115200)
	saber = Sabertooth(port, baudrate=38400)

	try:
		print('temperature [C]: {}'.format(saber.textGet('m2:gett')))
		print('battery [mV]: {}'.format(saber.textGet('m2:getb')))
		saber.text('m1:startup')
		saber.text('m2:startup')
		for speed in range(-100, 100, 20):
			saber.drive(1, speed)
			saber.drive(2, speed)

			# format returned text
			m1 = saber.textGet('m1:get').split()[1]
			m2 = saber.textGet('m2:get').split()[1]
			print('M1: {:6} M2: {:6}'.format(m1, m2))
			time.sleep(1)

	except KeyboardInterrupt:
		print('keyboard interrupt ... ')


	saber.drive(1, 0)
	saber.drive(2, 0)
	time.sleep(0.1)
	saber.stop()


if __name__ == '__main__':
	packet()
	# ascii()
