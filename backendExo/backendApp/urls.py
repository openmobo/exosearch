from django.urls import  path,include
from backendApp.views import LogUploadViewSet
from rest_framework import routers
from .views import ForwarderDataViewSet

router=routers.DefaultRouter()
router.register(r'Data', LogUploadViewSet)
router.register(r'forwarder-data', ForwarderDataViewSet)



urlpatterns=[
    path('',include(router.urls)),
   
]