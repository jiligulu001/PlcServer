from __future__ import unicode_literals
from __future__ import division

from django.db import models
import threading
import os
import random
import datetime
from time import ctime
import sys,struct
import re
import MySQLdb
from collections import defaultdict
import time
from django.contrib.auth.models import User
import cPickle as pickle 
import ConfigParser


"""insert device id to database"""
def insertDeviceId():
	cf = ConfigParser.ConfigParser()
	cf.read("data.ini")
	device_id = cf.get("device","device_id")
	print "device_id : %s" %(device_id)



# class PlcData2(models.Model):
# 	CurTime = models.DateTimeField(default = 0)
# 	TEMP = models.CharField(max_length=32)
# 	Jacket_TEMP = models.CharField(max_length=32)
# 	DO = models.CharField(max_length=32)
# 	pH = models.CharField(max_length=32)
# 	O2 = models.CharField(max_length=32)
# 	Mix = models.CharField(max_length=32)
# 	Jacket_SV = models.CharField(max_length=32) 
# 	Base = models.CharField(max_length=32)
# 	device_id = models.ForeignKey(Device,related_name = 'PlcData2',default = 0)

# 	class Meta:
# 		db_table = 'PlcData2'
		
class Plc_data_one(models.Model):
	deviceName = models.CharField(max_length = 20,default = None,unique = True)
	currentDate = models.DateTimeField(default = 0,primary_key = True)
	temp = models.FloatField()
	dO = models.FloatField()
	pH = models.FloatField()
	stir = models.FloatField()
	feed = models.FloatField()
	acid = models.FloatField()
	base = models.FloatField()
	ca = models.FloatField()
	o2 = models.FloatField()
	n2 = models.FloatField()
	co2 = models.FloatField()
	class Meta:
		db_table = 'Plc_data_one'

class Plc_data_one_settings(models.Model):
	deviceName = models.CharField(max_length = 20,default = None,unique=True)
	currentDate = models.DateTimeField(default = 0,primary_key = True)
	temp = models.FloatField()
	dO = models.FloatField()
	pH = models.FloatField()
	stir = models.FloatField()
	feed = models.FloatField()
	acid = models.FloatField()
	tempSwitch = models.CharField(max_length = 1)
	doSwitch = models.CharField(max_length = 1)
	phSwitch = models.CharField(max_length =1)
	stirSwitch = models.CharField(max_length = 1)
	feedSwitch = models.CharField(max_length = 1)
	acidSwitch = models.CharField(max_length = 1)
	class Meta:
		db_table = 'Plc_data_one_settings'

   
class PlcTestSettingTb(models.Model):
	deviceName = models.CharField(max_length = 20,default = None,unique=True)
	currentDate = models.DateTimeField(default = 0)
	temp = models.FloatField()
	pH = models.FloatField()
	stir = models.FloatField()

	class Meta:
		db_table = 'TestSetting'