"""plc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
# from demo.views import PlcDataSingle,plcdata_single
from plcProject.views import UserList,UserDetail,plcdata_single
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
admin.autodiscover()


# router.register(r'users',views.UserViewSet)
# router.register(r'groups',views.GroupViewSet)

urlpatterns = [
 #    url(r'^users/$',UserList.as_view()),
 #    url(r'^users/(?P<pk>[0-9]+)/$',UserDetail.as_view()),
 #    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
	# # url(r'^',include(router.urls)),
      url(r'^admin/', admin.site.urls),
      url(r'^plcdata_single/$',plcdata_single),
 #    url(r'^plcdata/$',PlcDataList.as_view()),
 #    url(r'^plc2data/$',Plc2DataList.as_view()),
      url(r'^',include('plcProject.urls')),
    #url(r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root':'c:/Users/Administrator/Desktop/plc/static'})
]

urlpatterns += [
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework'))
]
