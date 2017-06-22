from django.contrib import admin
from plcProject.models import Plc_data_one,Plc_data_one_settings,PlcTestSettingTb
# Register your models here.

#admin.site.register(Device)
admin.site.register(Plc_data_one)
admin.site.register(Plc_data_one_settings)
admin.site.register(PlcTestSettingTb)