from django.shortcuts import get_object_or_404
from .serializers import *

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class KometarzeObrazkaViewSet(viewsets.ViewSet):
    serializer_class = KometarzSerializer

    def retrieve(self, request, pk=None):
        obrazek = get_object_or_404(Obrazek, id=pk)
        queryset = obrazek.kometarz_set.all().order_by('-data_publikacji')
        serializer = KometarzSerializer(queryset,many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = KometarzSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OcenyObrazkaViewSet(viewsets.ViewSet):
    serializer_class = OcenySerializer


    def retrieve(self, request, pk=None):
        obrazek = get_object_or_404(Obrazek, id=pk)
        queryset = obrazek.oceny_set.all()
        serializer = OcenySerializer(queryset,many=True)
        return Response(serializer.data)

    def create(self, request):


        serializer = OcenySerializer(data=request.data)


        if serializer.is_valid():
            obrazek = serializer.validated_data['obrazek']
            if not obrazek.czy_ocenil(serializer.validated_data['autor'].id):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ViewSet):
    serializer_class = UserProfileSerializer


    def retrieve(self, request, pk=None):
        queryset = User.objects.get(id=pk)
        serializer = UserProfileSerializer(queryset)
        return Response(serializer.data)
