from rest_framework import routers
from dsl_broker.views import health
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
# router = routers.DefaultRouter()
# router.register(r'health', IoTAgentHealthViewSet, basename='health')
# urlpatterns = [
#     url(r'health', include((router.urls, 'comunication_layer'))),
# ]

urlpatterns = [
    path('health/', health),
]
urlpatterns = format_suffix_patterns(urlpatterns)