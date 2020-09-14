from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
import requests
from rest_framework import status
import time
from rest_framework.decorators import api_view

MAX_RETRIES = 5
@api_view(['GET'])
def health(request):
    if request.method == "GET":
        attempt_num = 0  # keep track of how many times we've retried
        while attempt_num < MAX_RETRIES:
            r = requests.get('http://localhost:4041/iot/about', timeout=10)
            if r.status_code == 200:
                data = r.json()
                return Response(data, status=status.HTTP_200_OK)
            else:
                attempt_num += 1
                # You can probably use a logger to log the error here
                time.sleep(5)  # Wait for 5 seconds before re-trying
        return Response({"error": "Request failed"}, status=r.status_code)
    else:
        return Response({"error": "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST)