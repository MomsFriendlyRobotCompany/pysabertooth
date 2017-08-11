##
# Sabertooth.py: Class implementing packetized serial control of
#                Sabertooth 2x60 motor driver (Dimension Engineering).
#
# Copyright 2015, Egan McComb
#
# This code was adapted from MIT licensed:
#
# > Sabertooth.py
# > Copyright 2014, Troy Dack
# > <https://github.com/tdack/BBB-Bot>.
#
##
#
# Additional changes and update
#
# copywrite 2017 Kevin J. Walchko
#
##

from __future__ import division
import serial
import logging
import time


class Sabertooth(object):
	"""
	Sabertooth: A class to control a Sabertooth 2x60 using the packetized
				serial mode (DIP switches 1,2 low).

	https://www.dimensionengineering.com/datasheets/Sabertooth2x60.pdf
	"""
	# Commands to implement. See pages 20-23 of the documentation for
	# additional commands available.
	# cmds = {
	# 	"fwd_left": 0x00,
	# 	"rev_left": 0x01,
	# 	"fwd_right": 0x04,
	# 	"rev_right": 0x05,
	# 	"fwd_mixed": 0x08,
	# 	"rev_mixed": 0x09,
	# 	"right_mixed": 0x0A,
	# 	"left_mixed": 0x0B,
	# 	"ramp": 0x10
	# }

	FORWARD_1 = 0x00
	REVERSE_1 = 0x01
	FORWARD_2 = 0x04
	REVERSE_2 = 0x05
	FORWARD_MIXED = 0x08
	REVERSE_MIXED = 0x09
	RIGHT_MIXED = 0x0A
	LEFT_MIXED = 0x0B
	RAMP = 0x10
	# "fwd_mixed": 0x08,
	# "rev_mixed": 0x09,
	# "right_mixed": 0x0A,
	# "left_mixed": 0x0B,
	# "ramp": 0x10

	def __init__(self, port, baudrate=9600, address=128, timeout=0.1):
		"""
		port:        Teletypewriter device to connect to.
		address:     Address of controller to send commands to
					 (set by DIP switches 3-6).

		"""
		self.port = port
		self.address = address

		# if (self.port is None) or (self.address < 128 or self.address > 135):
		# 	return None
		if 128 > self.address > 135:
			raise Exception('PySabertooth, invalid address: {}'.format(address))

		# if baudrate in [9600, 19200, 38400, 115200]:
		# 	pass
		# else:
		# 	raise Exception('PySabertooth, invalid baudrate {}'.format(baudrate))

		# Initialize serial port.
		self.saber = serial.Serial()
		self.saber.baudrate = baudrate
		self.saber.port = port
		self.saber.timeout = timeout

		self.open()
		self.setBaudrate(baudrate)

		print('')
		print('='*40)
		print('Sabertooth Motor Controller')
		print('  port: {}'.format(self.saber.port))
		print('  baudrate: {}  bps'.format(self.saber.baudrate))
		print('  address: {}'.format(self.address))
		print('-'*40)
		print('')

	def __del__(self):
		self.stop()
		self.close()
		return

	def close(self):
		self.saber.close()

	def setBaudrate(self, baudrate):
		valid = {
			2400:   1,
			9600:   2,
			19200:  3,
			38400:  4,
			115200: 5
		}
		# if baudrate in [9600, 19200, 38400, 115200]:
		# 	pass
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
		if not self.saber.is_open:
			self.saber.open()
		self.saber.write(b'\xaa')
		self.saber.write(b'\xaa')
		time.sleep(0.2)

	def sendCommand(self, command, message):
		"""
		sendCommand: Sends a packetized serial command to the Sabertooth
					 controller, returning bytes written.

			command: Command to send. Valid commands (as strings) are:
				fwd_left
				rev_left
				fwd_right
				rev_right
				fwd_mixed
				rev_mixed
				right_mixed
				left_mixed
				ramp
			message: Command content, usually speed 0-100%.

		"""
		# Calculate checksum termination (page 23 of the documentation).
		checksum = (self.address + command + message) & 127
		# Write data packet.
		msg = [self.address, command, message, checksum]
		msg = bytes(bytearray(msg))
		# sentBytes = self.saber.write("".join(chr(i) for i in [self.address, command, message, checksum]))
		self.saber.write(msg)
		# Flush UART.
		self.saber.flush()
		# return sentBytes

#	def mixedDrive(self, dir_surge="fwd", speed_surge=0, dir_yaw="left", speed_yaw=0):
#		"""
#		mixedDrive: Mixed drive (additive differential drive).
#					Calls sendCommand, returning bytes written.
#
#			dir_surge:   fwd or rev
#			speed_surge: 0-100% (surge)
#			dir_yaw:     left or right (additive)
#			speed_yaw:   0-100% (yaw)
#		"""
#		# Stupidity checks.
#		validcmds = ["fwd", "rev"]
#		if (dir_surge not in validcmds):
#			return -1
#
#		validcmds = ["left", "right"]
#		if (dir_yaw not in validcmds):
#			return -1
#
#		if speed_surge < 0:
#			speed_surge = 0
#		elif speed_surge > 100:
#			speed_surge = 100
#
#		if speed_yaw < 0:
#			speed_yaw = 0
#		elif speed_yaw > 100:
#			speed_yaw = 100
#
#		# Calculate speed command from percentage.
#		speed_surge = int(speed_surge*127/100)
#		speed_yaw = int(speed_yaw*127/100)
#
#		logging.debug("mixedDrive: %s %d %s %d".format(dir_surge + "_mixed", speed_surge, dir_yaw + "_mixed", speed_yaw))
#
#		# sentBytes = self.sendCommand(self.cmds[dir_surge + "_mixed"], speed_surge)
#		# sentBytes += self.sendCommand(self.cmds[dir_yaw + "_mixed"], speed_yaw)
#		# return sentBytes

	def stop(self):
		"""
			stop: Stops both motors using independentDrive, returning bytes written.

		"""
		sentBytes = 0
		#sentBytes = self.independentDrive("fwd", 0, "fwd", 0)
		self.driveBoth(0,0)
		return sentBytes

	# def setRamp(self, value):
	# 	"""
	# 	setRamp: Set acceleration ramp for controller.
	#
	# 		value: Ramp value to use (see documentation):
	# 			01-10: Fast Ramp
	# 			11-20: Slow Ramp
	# 			21-80: Intermediate Ramp
	#
	# 	"""
	# 	sentBytes = 0
	# 	if (value > 0 and value < 81):
	# 		sentBytes = self.sendCommand(self.cmds["ramp"], value)
	# 	else:
	# 		return -1
	#
	# 	return sentBytes

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
