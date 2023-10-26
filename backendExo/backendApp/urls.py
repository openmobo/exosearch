from django.urls import  path,include
from backendApp.views import LogUploadViewSet
from rest_framework import routers
from .views import ForwarderDataViewSet,RegisterView,LoginView,UserView,LogoutView

router=routers.DefaultRouter()
router.register(r'Data', LogUploadViewSet)
router.register(r'forwarder-data', ForwarderDataViewSet)





urlpatterns=[
    path('',include(router.urls)),

    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    
   
]