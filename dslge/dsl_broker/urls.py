from rest_framework import routers
from dsl_broker.views import health, configure
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

urlpatterns = [
    path('health/', health),
    path('configure/', configure),
]
urlpatterns = format_suffix_patterns(urlpatterns)
