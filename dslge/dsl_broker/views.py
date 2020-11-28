from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
import requests
from rest_framework import status
import time
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from dsl_broker.models import EntityModel, Model
from dsl_broker.services.creators.entity_model_creator import EntityModelCreator


MAX_RETRIES = 5
EXTERNAL_BASIC_URL = 'http://localhost:1026'
BASIC_URL = 'http://localhost:8000/api/'


def send_get_request(route, headers=None):
    attempt_num = 0  # keep track of how many times we've retried
    while attempt_num < MAX_RETRIES:
        if headers:
            headers = {'Connection': 'Keep-Alive', 'fiware-service': 'openiot', 'fiware-servicepath': '/'} 
            response = requests.get(EXTERNAL_BASIC_URL + route, headers=headers, timeout=10)
        else:
            response = requests.get(EXTERNAL_BASIC_URL + route, timeout=10)
        if response.status_code == status.HTTP_200_OK:
            return response.json(), response
        else:
            attempt_num += 1
            # You can probably use a logger to log the error here
            time.sleep(5)  # Wait for 5 seconds before re-trying
    return None


def send_post_request(route, data):
    attempt_num = 0  # keep track of how many times we've retried
    while attempt_num < MAX_RETRIES:
        response = requests.post(EXTERNAL_BASIC_URL + route, json=data)
        if response.status_code == status.HTTP_201_CREATED:
            return response
        else:
            attempt_num += 1
            # You can probably use a logger to log the error here
            time.sleep(5)  # Wait for 5 seconds before re-trying
    return None


@api_view(['GET'])
def health(request):
    if not request.method == 'GET':
        return Response({"error": "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST)
    data, req = send_get_request('/version/')
    return Response(data, status=status.HTTP_200_OK) if req.status_code == status.HTTP_200_OK \
        else Response({"error": "Request failed"}, status=req.status_code)


@api_view(['POST'])
def configure(request):
    if not request.method == 'POST':
        return Response({"error": "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST)
    request_data = request.data
    headers = request.headers
    get_response = send_get_request('/v2/entities/'+request_data['id'], headers)
    if not get_response[1].status_code == status.HTTP_200_OK:
        return Response({"error": "Request failed"}, status=get_response[1].status_code)
    creator = EntityModelCreator(request_data)
    post_response = send_post_request(
        '/v2/subscriptions/', make_subscritption_data(request_data))
    if not post_response is None:
        creator.save()
        return Response({"succcess": "Configuration done."}, status=status.HTTP_200_OK) \
            if (not creator.errors and post_response.status_code == status.HTTP_201_CREATED) \
            else Response({"error": creator.errors}, status=post_response.status_code)
    return Response({"error": "Middleware is not responding."})

@api_view(['POST'])
def notification(request):
    return Response(request.data)

def make_subscritption_data(data_info):
    data = {
        "description": "Notify me of all measure changes",
        "subject": {
            "entities": [
                {
                    "idPattern": ".*",
                    "type": "{}".format(data_info['type'])
                }
            ],
            "condition": {
                'attrs': ["count"]
            }
        },
        "notification": {
            "http": {
                # "url": "{}".format((BASIC_URL + 'measures/' + data_info['id']))
                "url": "{}".format((BASIC_URL + 'notification/'))
            }
        }
    }
    return data
