from django.urls import path, include
from . import views
from rest_framework import routers, renderers


router = routers.DefaultRouter()
router.register('eventsList', views.EventView, basename='Event')
router.register('registrations', views.RegistrationManage, basename='RegistrationManage')
router.register('registrationDetails', views.RegistrationDetails, basename='RegistrationDetails')
router.register('events', views.EventManage, basename='EventManage')

urlpatterns = [
    path('', include(router.urls)),
    path('signUpEvent/', views.register_new, name='signUpEvent'),
]
