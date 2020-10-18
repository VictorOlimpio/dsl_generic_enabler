from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
import requests
from rest_framework import status
import time
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes


MAX_RETRIES = 5
BASIC_URL = 'http://localhost:1026'

def send_request(route):
    attempt_num = 0  # keep track of how many times we've retried
    while attempt_num < MAX_RETRIES:
        r = requests.get(BASIC_URL + route, timeout=10)
        if r.status_code == 200:
            return r.json(), r
        else:
            attempt_num += 1
            # You can probably use a logger to log the error here
            time.sleep(5)  # Wait for 5 seconds before re-trying
    return None

@api_view(['GET'])
def health(request):
    if request.method == 'GET':
        data, req = send_request('/version/')
        return Response(data, status=status.HTTP_200_OK) if req.status_code == 200 \
        else Response({"error": "Request failed"}, status=req.status_code)
    else:
        return Response({"error": "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def configure(request):
    if request.method == 'POST':
        request_data = request.data
        data, req = send_request('/v2/entities/'+request.data['id'])
        if req.status_code == 200:
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Request failed"}, status=req.status_code)
    else:
        return Response({"error": "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST)
