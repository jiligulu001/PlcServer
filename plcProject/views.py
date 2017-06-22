from django.contrib.auth.models import User,Group
from plcProject.models import Plc_data_one,Plc_data_one_settings
from django.http import HttpResponse,Http404
from django.template.loader import get_template
from django.template import Context
import datetime
from django.shortcuts import render_to_response
from rest_framework import request
from rest_framework import viewsets 
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.reverse import reverse
from plcProject.serializers import PlcDataSerializer,UserSerializer,GroupSerializer,LoginSerializer,PlcDataSettingsSerializer
#from demo.permissions import IsOwnerOrReadOnly
from django.http import Http404
import json
from socket import *
import threading
import binascii,struct,time,MySQLdb
import string
from time import ctime,sleep
import libnodave
import ctypes
from ctypes import *
import Queue
import logging
import logging.config
#@csrf_exempt
#@api_view(['GET', 'POST'])
#from plcProject.tasks import write_to_plc,read_setting_value,read_data_fromplc


@permission_classes((permissions.AllowAny,))

class DeviceList(APIView):
	def get(self,request,format=None):
		getDatas = Device.objects.all()
		serializer = DeviceSerializer(getDatas,many=True)
		return Response(serializer.data)

class PlcTest(APIView):

	def get_object(self,pk):
		try:
			return Plc_data_one.objects.get(deviceName=pk)
		except Plc_data_one.DoesNotExist:
			raise Http404

	def get(self,request,pk,format=None):
		getDatas = self.get_object(pk)
		print "***********************use = %s" %request.user
		serializer = PlcDataSerializer(getDatas)

		return Response(serializer.data)
	
	def post(self,request,pk,format=None):
		getDatas = self.get_object(pk)
		
		#write_to_plc(request.data)
		
		serializer = PlcDataSerializer(getDatas,data = request.data,partial=True)
		
		if serializer.is_valid():
			#serializer.update()
			serializer.save()
			return Response(serializer.data,status=status.HTTP_201_CREATED)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PlcTestSettings(APIView):
	def __init__(self):
		self.que = Queue.Queue()
		self.change_id = 0

	def get_object(self,pk):
		try:
			return Plc_data_one_settings.objects.get(deviceName=pk)
		except Plc_data_one_settings.DoesNotExist:
			raise Http404

	def get(self,request,pk,format=None):
		#read_setting_value()
		getDatas = self.get_object(pk)
		#PlcTestTb.objects.filter(deviceName = pk).update(temp = 11.11)
		serializer = PlcDataSettingsSerializer(getDatas)

		return Response(serializer.data)
	
	def post(self,request,pk,format=None):
		getDatas = self.get_object(pk)
		#print "self que = %s" %(self.que)
		#write_to_plc(request.data)
		logger.debug("%s update %s"%(request.user,request.data))
		t_write = threading.Thread(target = write_to_plc,args = [request.data])
		t_write.start()
		#self.que.put(write_to_plc(request.data))
		
		#read_setting_value()
		serializer = PlcDataSettingsSerializer(getDatas,data = request.data,partial=True)
		
		if serializer.is_valid():
		 	serializer.save()
		 	return Response(serializer.data,status=status.HTTP_201_CREATED)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PlcTest2(APIView):
	
	def get_object(self,pk):
		try:
			return PlcTestTb.objects.get(deviceName=pk)
		except PlcTestTb.DoesNotExist:
			raise Http404

	def get(self,request,format=None):
		getDatas = Plc_data_one.objects.all()

		#PlcTestTb.objects.filter(deviceName = pk).update(temp = 11.11)
		serializer = PlcDataSerializer(getDatas,many = True)

		return Response(serializer.data)
	
	# def put(self,request,pk,format=None):
	# 	getDatas = self.get_object(pk = pk)
	# 	serializer = PlcTestSerializer(getDatas,data = request.data,partial = True)
	# 	if serializer.is_valid():
	# 		#serializer.update()
	# 		serializer.save()
	# 		return Response(serializer.data,status=status.HTTP_201_CREATED)
	# 	return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class JSONResponse(HttpResponse):
    
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
		
class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
	queryset = Group.objects.all()
	serializer_class = UserSerializer

def plcdata_single(request):
	
	plcdata = PlcData.objects.order_by('-id').first()
	#serializer = PlcDataSerializer(plcdata)
	#return Response(serializer.data)
	return render_to_response('current_datetime.html',{'TEMP':plcdata.TEMP,'Jacket_TEMP':plcdata.Jacket_TEMP,'DO':plcdata.DO,'pH':plcdata.pH,'O2':plcdata.O2,'Mix':plcdata.Mix,'Jacket_SV':plcdata.Jacket_SV,'Base':plcdata.Base})

class LoginViewSet(APIView):
	#queryset = User.objects.all()
	#print queryset
	def post(self,request,format=None):
		username = request.data.get('username')
		password = request.data.get('password')
		user = User.objects.get(username__iexact=username)
		print password
		if user.check_password(password):	
			print user 
			serializer = LoginSerializer(user,data = request.data)
			if serializer.is_valid():
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(status=status.HTTP_400_BAD_REQUEST)
		return Response(status = status.HTTP_404_NOT_FOUND)

def read_data_fromplc():
	dave = libnodave.libnodave()
	dave.open_socket("192.168.6.14")
	dave.new_interface("test",0,122,1)
	dave.init_adapter()
	dave.connect_plc(0,0,1)
	print "from dave = %s" %dave
	bf = ctypes.c_short(0)
	bf_p = ctypes.pointer(bf)
	bf_float = ctypes.c_float(11.29)
	#bb = ctypes.c_float(a.myToPlcFloat(11.29))
	#print type(bb)
	while True:
		sleep(5)
		temp = ctypes.c_float(0.0)
		do = ctypes.c_float(0.0)
		pH = ctypes.c_float(0.0)
		stir = ctypes.c_float(0.0)
		feed = ctypes.c_float(0.0)
		acid = ctypes.c_float(0.0)
		base = ctypes.c_float(0.0)
		ca = ctypes.c_float(0.0)
		o2 = ctypes.c_float(0.0)
		n2 = ctypes.c_float(0.0)
		co2 = ctypes.c_float(0.0)
		
		dave.read_bytes(0x84,1,16,4,byref(temp))
		dave.read_bytes(0x84,10,16,4,byref(do))
		dave.read_bytes(0x84,25,16,4,byref(pH))
		dave.read_bytes(0x84,30,36,4,byref(stir))
		dave.read_bytes(0x84,30,0,4,byref(feed))
		dave.read_bytes(0x84,30,4,4,byref(acid))
		dave.read_bytes(0x84,25,142,4,byref(base))
		dave.read_bytes(0x84,10,108,4,byref(ca))
		dave.read_bytes(0x84,10,112,4,byref(o2))
		dave.read_bytes(0x84,10,116,4,byref(n2))
		dave.read_bytes(0x84,25,84,4,byref(co2))
	

		temp = round(dave.myToPlcFloat(temp),2)
		do = round(dave.myToPlcFloat(do),2)
		pH = round(dave.myToPlcFloat(pH),2)
		stir = dave.myToPlcFloat(stir)
		feed = round(dave.myToPlcFloat(feed),2)
		acid = round(dave.myToPlcFloat(acid),2)
		base = round(dave.myToPlcFloat(base),2)
		ca = round(dave.myToPlcFloat(ca),2)
		o2 = round(dave.myToPlcFloat(o2),2)
		n2 = round(dave.myToPlcFloat(n2),2)
		co2 = round(dave.myToPlcFloat(co2),2)
		

		print "temp = %s do = %s pH = %s stir = %s feed = %s acid = %s base = %s ca = %s o2 = %s n2 = %s co2 = %s"%(temp,do,pH,stir,feed,acid,base,ca,o2,n2,co2)
		name = 'br20140010'
		conn = cur = None
		try:
			conn = MySQLdb.connect(host='127.0.0.1',user = 'root',passwd = '123456',db = 'plcdb')
			cur = conn.cursor()
			cur.execute("REPLACE INTO plc_data_one(deviceName,currentDate,temp,do,pH,stir,feed,acid,base,ca,o2,n2,co2) VALUES(%s,NOW(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,temp,do,pH,stir,feed,acid,base,ca,o2,n2,co2))
		except MySQLdb.Error as e:
			raise e
		finally:
			if cur:
				cur.close()
			if conn:
				conn.commit()
				conn.close()
	dave.disconnect()

def write_to_plc(sendData = None):
	#print "send data  = %s type = %s" %(sendData,type(sendData))
	dave = libnodave.libnodave()
	dave.open_socket("192.168.6.14")
	dave.new_interface("test",0,122,1)
	dave.init_adapter()
	dave.connect_plc(0,0,1)

	try:
		temp = sendData["temp"]	
		ftemp = float(temp.encode())
		result = dave.write_bytes(0x84,1,40,4,byref(ctypes.c_float(dave.myToPlcFloat(ftemp))))
	except KeyError as e:
		print e
	try:
		do = sendData["do"]
		print type(float(do.encode()))
		fdo = float(do.encode())
		result = dave.write_bytes(0x84,10,52,4,byref(ctypes.c_float(dave.myToPlcFloat(fdo))))
	except KeyError as e:
		print e
	try:
		pH = sendData["pH"]
		fpH = float(pH.encode())
		result = dave.write_bytes(0x84,25,52,4,byref(ctypes.c_float(dave.myToPlcFloat(fpH))))
	except KeyError as e:
		print e
	try:
		stir = sendData["stir"]
		fstir = float(stir.encode())
		result = dave.write_bytes(0x84,30,20,4,byref(ctypes.c_float(dave.myToPlcFloat(fstir))))
	except Exception as e:
		print e
	try:
		feed = sendData["feed"]
		ffeed = float(feed.encode())
		result = dave.write_bytes(0x84,30,12,4,byref(ctypes.c_float(dave.myToPlcFloat(ffeed))))
	except KeyError as e:
		print e
	try:
		acid = sendData["acid"]
		facid = float(acid.encode())
		result = dave.write_bytes(0x84,30,16,4,byref(ctypes.c_float(dave.myToPlcFloat(ffeed))))
	except KeyError as e:
		print e
	
	try:
		temp_switch = sendData["tempSwitch"]
		temp = c_short()
		cj_lock.acquire()
		res = dave.read_bytes(0x84,8,0,1,byref(temp))
		tt = libnodave.int_to_bitarr(temp.value)
		print "tt = %s temp_switch = %s type switch = %s"%(tt,temp_switch,type(temp_switch))
		tt[1] = temp_switch
		print " change tt = %s" %tt
		tt = libnodave.bitarr_to_int(tt)
		dave.write_bytes(0x84,8,0,1,byref(c_short(tt)))
		cj_lock.release()
	except Exception as e:
		print e
	try:
		do_switch = sendData["doSwitch"]
		temp = c_short()
		cj_lock.acquire()
		res = dave.read_bytes(0x84,8,0,1,byref(temp))
		tt = libnodave.int_to_bitarr(temp.value)
		tt[2] = do_switch
		print " change tt = %s" %tt
		tt = libnodave.bitarr_to_int(tt)
		dave.write_bytes(0x84,8,0,1,byref(c_short(tt)))
		cj_lock.release()
	except Exception as e:
		print e
	try:
		ph_switch = sendData["phSwitch"]
		temp = c_short()
		cj_lock.acquire()
		res = dave.read_bytes(0x84,8,0,1,byref(temp))
		tt = libnodave.int_to_bitarr(temp.value)
		tt[3] = ph_switch
		tt = libnodave.bitarr_to_int(tt)
		print "*****************ph = %s"%(bin(tt))
		dave.write_bytes(0x84,8,0,1,byref(c_short(tt)))
		cj_lock.release()
	except Exception as e:
		print e
	try:
		stir_switch = sendData["stirSwitch"]
		temp = c_short()
		cj_lock.acquire()
		res = dave.read_bytes(0x84,8,0,1,byref(temp))
		tt = libnodave.int_to_bitarr(temp.value)
		tt[4] = stir_switch
		tt = libnodave.bitarr_to_int(tt)
		dave.write_bytes(0x84,8,0,1,byref(c_short(tt)))
		cj_lock.release()
	except Exception as e:
		print e
	try:
		feed_switch = sendData["feedSwitch"]
		temp = c_short()
		cj_lock.acquire()
		res = dave.read_bytes(0x84,8,0,1,byref(temp))
		tt = libnodave.int_to_bitarr(temp.value)
		tt[5] = feed_switch
		tt = libnodave.bitarr_to_int(tt)
		dave.write_bytes(0x84,8,0,1,byref(c_short(tt)))
		cj_lock.release()
	except Exception as e:
		print e
	try:
		acid_switch = sendData["acidSwitch"]
		temp = c_short()
		cj_lock.acquire()
		res = dave.read_bytes(0x84,8,0,1,byref(temp))
		tt = libnodave.int_to_bitarr(temp.value)
		tt[6] = acid_switch
		tt = libnodave.bitarr_to_int(tt)
		print "*****************ph = %s"%(bin(tt))
		dave.write_bytes(0x84,8,0,1,byref(c_short(tt)))
		cj_lock.release()
	except Exception as e:
		print e
	dave.disconnect()

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
	feed = ctypes.c_float(0.0)
	acid = ctypes.c_float(0.0)
	switch_value = ctypes.c_short(0)

	bf = ctypes.c_short(0)
	bf_p = ctypes.pointer(bf)
	bf_float = ctypes.c_float(11.29)
	dave.read_bytes(0x84,1,40,4,byref(temp))
	dave.read_bytes(0x84,10,52,4,byref(do))
	dave.read_bytes(0x84,25,52,4,byref(pH))
	dave.read_bytes(0x84,30,20,4,byref(stir))
	dave.read_bytes(0x84,30,12,4,byref(feed))
	dave.read_bytes(0x84,30,16,4,byref(acid))
	dave.read_bytes(0x84,8,0,1,byref(switch_value))
	print "switch_value = %s" %switch_value.value
	temp_list = libnodave.int_to_bitarr(switch_value.value)
	
	temp = round(dave.myToPlcFloat(temp),2)
	do = round(dave.myToPlcFloat(do),2)
	pH = round(dave.myToPlcFloat(pH),2)
	stir = dave.myToPlcFloat(stir)
	feed = round(dave.myToPlcFloat(feed),2)
	acid = round(dave.myToPlcFloat(feed),2)
	temp_switch = temp_list[1]
	do_switch = temp_list[2]
	ph_switch = temp_list[3]
	stir_switch = temp_list[4]
	feed_switch = temp_list[5]
	acid_switch = temp_list[6]
	print "******* SV: temp = %s do = %s ph = %s stir = %s feed = %s acid = %s " %(temp,do,pH,stir,feed,acid)
	name = 'br20140010'
	conn = cur = None
	try:
		conn = MySQLdb.connect(host='127.0.0.1',user = 'root',passwd = '123456',db = 'plcdb')
		cur = conn.cursor()
		cur.execute("REPLACE INTO  plc_data_one_settings(deviceName,currentDate,temp,do,pH,stir,feed,acid,tempSwitch,doSwitch,phSwitch,stirSwitch,feedSwitch,acidSwitch) VALUES(%s,NOW(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,temp,do,pH,stir,feed,acid,temp_switch,do_switch,ph_switch,stir_switch,feed_switch,acid_switch))
	except MySQLdb.Error as e:
		raise e
	finally:
		if cur:
			cur.close()
		if conn:
			conn.commit()
			conn.close()
	dave.disconnect()

# dave = libnodave.libnodave()
# dave.open_socket("192.168.6.14")
# dave.new_interface("test",0,122,1)
# dave.init_adapter()
# dave.connect_plc(0,0,1)
logging.config.fileConfig("./logging.conf")
logger_name = "actionsLog"
logger = logging.getLogger(logger_name)
cj_lock = threading.Lock()
threads_list = []
thread_read_data = threading.Thread(target=read_data_fromplc)
threads_list.append(thread_read_data)
for t in threads_list:
	t.setDaemon(True)
	#t.start()