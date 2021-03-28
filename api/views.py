from django.shortcuts import get_object_or_404
from widok.models import Obrazek
from users.models import User

from .serializers import KometarzSerializer, OcenySerializer, UserProfileSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ObrazekViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = OcenySerializer

    @action(detail=True, methods=['get', 'post'])
    def komentarze(self, request, pk=None):

        if request.method == 'GET':
            queryset = get_object_or_404(Obrazek, id=pk).kometarz_set.order_by('-data_publikacji')

            serializer = KometarzSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            serializer = KometarzSerializer(data=request.data, context={'id': pk,'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'post'])
    def oceny(self, request, pk=None):

        if request.method == 'GET':
            queryset = get_object_or_404(Obrazek, id=pk).oceny_set
            serializer = OcenySerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            serializer = OcenySerializer(data=request.data, context={'id': pk,'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserProfileViewSet(viewsets.ViewSet):
    serializer_class = UserProfileSerializer

    def retrieve(self, request, pk=None):
        queryset = User.objects.get(id=pk)
        serializer = UserProfileSerializer(queryset)
        return Response(serializer.data)
