from rest_framework import routers
from dsl_broker.views import health, configure, notification
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

urlpatterns = [
    path('health/', health),
    path('configure/', configure),
    path('notification/', notification)
]
urlpatterns = format_suffix_patterns(urlpatterns)
