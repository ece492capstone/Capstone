#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Original Author: bastianraschke
Weblink: https://github.com/bastianraschke/pyfingerprint
Last Updated Date: Feb 15, 2019
Contents of file:
	1. create a fingerprint record
'''
"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""

import time,requests
from pyfingerprint.pyfingerprint import PyFingerprint

## Enrolls new finger
##

## Tries to initialize the sensor
def enroll_fingerprint():
	try:
		f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

		if ( f.verifyPassword() == False ):
			raise ValueError('The given fingerprint sensor password is wrong!')

	except Exception as e:
		print('The fingerprint sensor could not be initialized!')
		print('Exception message: ' + str(e))
		exit(1)

	## Gets some sensor information
	print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

	## Tries to enroll new finger
	try:
		print('Waiting for finger...')

		## Wait that finger is read
		while ( f.readImage() == False ):
			pass

		## Converts read image to characteristics and stores it in charbuffer 1
		f.convertImage(0x01)

		## Checks if finger is already enrolled
		result = f.searchTemplate()
		positionNumber = result[0]

		if ( positionNumber >= 0 ):
			print('Template already exists at position #' + str(positionNumber))
			#post msg to website
			url1 = "http://0.0.0.0:4310/register"
			data1 = {'positionNumber': positionNumber,"goToSignUp":0}
			r = requests.post(url1, data1)
			url2 = "http://0.0.0.0:4311/exit"
			daya2 = {"mode":"1"}
			r2 = requests.post(url2,data2)
			#call search
			exit(0)

		print('Remove finger...')
		time.sleep(2)

		print('Waiting for same finger again...')

		## Wait that finger is read again
		while ( f.readImage() == False ):
			pass

		## Converts read image to characteristics and stores it in charbuffer 2
		f.convertImage(0x02)

		## Compares the charbuffers
		if ( f.compareCharacteristics() == 0 ):
			#~ raise Exception('Fingers do not match')
			enroll_fingerprint()
		
		## Creates a template
		f.createTemplate()

		## Saves template at new position number
		positionNumber = f.storeTemplate()
		print('Finger enrolled successfully!')
		print('New template position #' + str(positionNumber))
		
		#post msg to website:success
		url1 = "http://0.0.0.0:4310/register"
		data1 = {'positionNumber': positionNumber,"goToSignUp":1}
		r1 = requests.post(url1, data1)
		url2 = "http://0.0.0.0:4311/exit"
		daya2 = {"mode":"1"}
		r2 = requests.post(url2,data2)
		exit(0)
	except Exception as e:
		print('Operation failed!')
		print('Exception message: ' + str(e))
		exit(1)
		
if __name__=="__main__":
	enroll_fingerprint()
