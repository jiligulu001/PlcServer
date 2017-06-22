from __future__ import absolute_import 
from plc.celery import app
from celery import task
import MySQLdb
import libnodave
import ctypes
from ctypes import *



@task
def add(x,y):
	return x + y

@task
def read_data_fromplc():

	dave = libnodave.libnodave()
	dave.open_socket("192.168.6.14")
	dave.new_interface("test",0,122,1)
	dave.init_adapter()
	dave.connect_plc(0,0,1)

	temp = ctypes.c_float(0.0)
	j_temp = ctypes.c_float(0.0)
	do = ctypes.c_float(0.0)
	pH = ctypes.c_float(0.0)
	stir = ctypes.c_float(0.0)
	o2 = ctypes.c_float(0.0)
	base = ctypes.c_float(0.0)
	
	bf = ctypes.c_short(0)
	bf_p = ctypes.pointer(bf)
	bf_float = ctypes.c_float(11.29)
	#bb = ctypes.c_float(a.myToPlcFloat(11.29))
	#print type(bb)
	dave.read_bytes(0x84,1,16,4,byref(temp))
	dave.read_bytes(0x84,1,36,4,byref(j_temp))
	dave.read_bytes(0x84,10,16,4,byref(do))
	dave.read_bytes(0x84,25,16,4,byref(pH))
	dave.read_bytes(0x84,30,20,4,byref(stir))
	dave.read_bytes(0x84,10,112,4,byref(o2))
	dave.read_bytes(0x84,25,80,4,byref(base))

	temp = dave.myToPlcFloat(temp)
	j_temp = dave.myToPlcFloat(j_temp)
	do = dave.myToPlcFloat(do)
	pH = dave.myToPlcFloat(pH)
	stir = dave.myToPlcFloat(stir)
	o2 = dave.myToPlcFloat(o2)
	base = dave.myToPlcFloat(base)
	print "*******temp = %s j_temp = %s do = %s pH = %s stir = %s o2 = %s base = %s"%(temp,j_temp,do,pH,stir,o2,base)
	name = 'br20140010'
	conn = cur = None
	try:
		conn = MySQLdb.connect(host='127.0.0.1',user = 'root',passwd = '123456',db = 'plcdb')
		cur = conn.cursor()
		cur.execute("REPLACE INTO plc_data_one(deviceName,currentDate,temp,j_temp,do,pH,stir,o2,base) VALUES(%s,NOW(),%s,%s,%s,%s,%s,%s,%s)",(name,temp,j_temp,do,pH,stir,o2,base))
	except MySQLdb.Error as e:
		raise e
	finally:
		if cur:
			cur.close()
		if conn:
			conn.commit()
			conn.close()
			dave.disconnect()

@task
def write_to_plc(sendData = None):
	dave = libnodave.libnodave()
	dave.open_socket("192.168.6.14")
	dave.new_interface("test",0,122,1)
	dave.init_adapter()
	dave.connect_plc(0,0,1)
	# temp = ctypes.c_float(0.0)
	# pH = ctypes.c_float(0.0)
	# stir = ctypes.c_float(0.0)
	# bf = ctypes.c_short(0)
	# bf_p = ctypes.pointer(bf)
	#bf_float = ctypes.c_float(11.29)
	#bb = ctypes.c_float(a.myToPlcFloat(11.29))
	#print type(bb)
	
	try:
		temp = sendData["temp"]
		print "************************%s" %(temp.encode())
		print type(float(temp.encode()))
		ftemp = float(temp.encode())
		
		result = dave.write_bytes(0x84,1,40,4,byref(ctypes.c_float(dave.myToPlcFloat(ftemp))))
	except KeyError as e:
		print e
	try:
		do = sendData["do"]
		fdo = float(do.encode())
		result = dave.write_bytes(0x84,10,52,4,byref(ctypes.c_float(dave.myToPlcFloat(fdo))))
	except KeyError as e:
		print e
	try:
		pH = sendData["pH"]
		result = dave.write_bytes(0x84,25,52,4,byref(ctypes.c_float(dave.myToPlcFloat(pH))))
	except KeyError as e:
		print e
	try:
		stir = sendData["stir"]
		result = dave.write_bytes(0x84,30,20,4,byref(ctypes.c_float(dave.myToPlcFloat(stir))))
	except KeyError as e:
		print e


	dave.disconnect()
	

@task
def read_setting_value():
	dave = libnodave.libnodave()
	dave.open_socket("192.168.6.14")
	dave.new_interface("test",0,122,1)
	dave.init_adapter()
	dave.connect_plc(0,0,1)

	temp = ctypes.c_float(0.0)
	do = ctypes.c_float(0.0)
	pH = ctypes.c_float(0.0)
	stir = ctypes.c_float(0.0)
	
	bf = ctypes.c_short(0)
	bf_p = ctypes.pointer(bf)
	bf_float = ctypes.c_float(11.29)
	#bb = ctypes.c_float(a.myToPlcFloat(11.29))
	#print type(bb)
	dave.read_bytes(0x84,1,40,4,byref(temp))
	dave.read_bytes(0x84,10,52,4,byref(do))
	dave.read_bytes(0x84,25,52,4,byref(pH))
	dave.read_bytes(0x84,30,20,4,byref(stir))
	temp = dave.myToPlcFloat(temp)
	do = dave.myToPlcFloat(do)
	pH = dave.myToPlcFloat(pH)
	stir = dave.myToPlcFloat(stir)
	print "******* %s %s %s %s" %(temp,do,pH,stir)
	name = 'br20140010'
	conn = cur = None
	try:
		conn = MySQLdb.connect(host='127.0.0.1',user = 'root',passwd = '123456',db = 'plcdb')
		cur = conn.cursor()
		cur.execute("REPLACE INTO  plc_data_one_settings(deviceName,currentDate,temp,do,pH,stir) VALUES(%s,NOW(),%s,%s,%s,%s)",(name,temp,do,pH,stir))
	except MySQLdb.Error as e:
		raise e
	finally:
		if cur:
			cur.close()
		if conn:
			conn.commit()
			conn.close()
			dave.disconnect()

@task
def delloc_database():
	conn = cur = None
	try:
		conn = MySQLdb.connect(host='127.0.0.1',user = 'root',passwd = '123456',db = 'plcdb')
		cur = conn.cursor()
		cur.execute("TRUNCATE TABLE plc_data_one")
	except MySQLdb.Error as e:
		raise e
	finally:
		if cur:
			cur.close()
		if conn:
			conn.commit()
			conn.close()