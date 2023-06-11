from.models import Property
from.serializer import PropertySerializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_list_or_404
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView ,RetrieveUpdateDestroyAPIView


class PropertyAPiList(ListCreateAPIView):
    queryset=Property.objects.all()
    serializer_class = PropertySerializers



class PropertyAPiDetail(RetrieveUpdateDestroyAPIView):
    queryset=Property.objects.all()
    serializer_class = PropertySerializers