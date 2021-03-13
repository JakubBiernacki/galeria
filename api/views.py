from django.shortcuts import get_object_or_404
from .serializers import *

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# # Create your views here.
#
class KometarzeObrazkaViewSet(viewsets.ViewSet):
    serializer_class = KometarzSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


    def retrieve(self, request, pk=None):

        obrazek = get_object_or_404(Obrazek, id=pk)
        queryset = obrazek.kometarz_set.all().order_by('-data_publikacji')
        serializer = KometarzSerializer(queryset,many=True)
        return Response(serializer.data)

    def create(self, request):

        serializer = KometarzSerializer(data=request.data)

        if serializer.is_valid():

            if request.user != serializer.validated_data['autor']:
                return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OcenyObrazkaViewSet(viewsets.ViewSet):
    serializer_class = OcenySerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


    def retrieve(self, request, pk=None):
        obrazek = get_object_or_404(Obrazek, id=pk)
        queryset = obrazek.oceny_set.all()
        serializer = self.serializer_class(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def create(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            autor = serializer.validated_data['autor']
            if autor != request.user:
                return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

            obrazek = serializer.validated_data['obrazek']

            if not obrazek.czy_ocenil(autor.id):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ViewSet):
    serializer_class = UserProfileSerializer


    def retrieve(self, request, pk=None):
        queryset = User.objects.get(id=pk)
        serializer = UserProfileSerializer(queryset)
        return Response(serializer.data)
