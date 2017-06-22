
# -*- coding: utf-8
from __future__ import unicode_literals,absolute_import	
import json
from django.forms import widgets
from django.contrib.auth.models import User,Group
from rest_framework import serializers
from plcProject.models import Plc_data_one,Plc_data_one_settings




class UserSerializer(serializers.HyperlinkedModelSerializer):
	plcdata = serializers.PrimaryKeyRelatedField(many = True,read_only=True)
	class Meta:
		model = User
		fields = ('id','username','plcdata')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		mode = Group
		fields = ('url','username')

class PlcDataSerializer(serializers.ModelSerializer):
	#pk = serializers.ReadOnlyField()
	#owner =serializers.ReadOnlyField(source='owner.username')
	class Meta:
	 	model = Plc_data_one
	 	#owner = serializers.UserSerializer(read_only = True)
	 	fields = (['deviceName','currentDate','temp','dO','pH','stir','feed','acid','base','ca','o2','n2','co2'])

class PlcDataSettingsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Plc_data_one_settings
		fields = ('deviceName','currentDate','temp','dO','pH','stir','feed','acid','tempSwitch','doSwitch','phSwitch','stirSwitch','feedSwitch','acidSwitch')
# class DeviceSerializer(serializers.ModelSerializer):
# 	#PlcData1 = serializers.StringRelatedField(many=True)
# 	class Meta:
# 		model = Device
# 		fields = ('device_name',)


# class Plc2DataSerializer(serializers.ModelSerializer):
# 	#pk = serializers.ReadOnlyField()
# 	#owner =serializers.ReadOnlyField(source='owner.username')
# 	def restore_object(self,attrs,instance = None):
# 		if instance:
# 			instance.CurTime = attrs.get('CurTime',instance.CurTime)
# 			instance.TEMP = attrs.get('TEMP',instance.TEMP)
# 			instance.Jacket_TEMP = attrs.get('Jacket_TEMP',instance.Jacket_TEMP)
# 			instance.DO = attrs.get('DO',instance.DO)
# 			instance.pH = attrs.get('pH',instance.pH)
# 			instance.O2 = attrs.get('O2',instance.O2)
# 			instance.Mix = attrs.get('Mix',instance.Mix)
# 			instance.Jacket_SV = attrs.get('Jacket_SV',instance.Jacket_SV)
# 			instance.Base = attrs.get('Base',instance.Base)
# 			return instance
# 		return PlcData(**attrs)
# 	class Meta:
# 	 	model = PlcData2
# 	 	#owner = serializers.UserSerializer(read_only = True)
# 	 	fields = ('CurTime','TEMP','Jacket_TEMP','DO','pH','O2','Mix','Jacket_SV','Base')

class LoginSerializer(serializers.ModelSerializer):
	username = serializers.CharField(required=False,max_length=1024)
	password = serializers.CharField(required=False,max_length=1024)

	class Meta:
		model = User
		fields = ('username','password')
