from django.shortcuts import render
from django.http import JsonResponse
from web.models import Airport
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AirportSerializer
# Create your views here.

@api_view(['GET'])
def api(request):
    lists = Airport.objects.all()
    serialize = AirportSerializer(lists, many=True)

    return Response(serialize.data)