from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json


# Create your views here.

# Example Post Request
@api_view(["POST"])
def test(data):
    datareturn =json.loads(data.body)
    return JsonResponse(datareturn)

@api_view(["GET"])
def test(self):
    return Response("This is a get Request",status.HTTP_200_OK)
