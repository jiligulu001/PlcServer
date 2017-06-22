
from django.conf.urls import url,include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from plcProject import views
urlpatterns = [
	url(r'^test/$',views.PlcTest2.as_view()),
	url(r'^test/(?P<pk>[a-z0-9]+)/$',views.PlcTest.as_view()),
	url(r'^testSetting/(?P<pk>[a-z0-9]+)/$',views.PlcTestSettings.as_view()),
	url(r'^login/$',views.LoginViewSet.as_view()),
	url(r'^device/$',views.DeviceList.as_view()),
	url(r'^demo/$',views.plcdata_single),
]
urlpatterns = format_suffix_patterns(urlpatterns)
