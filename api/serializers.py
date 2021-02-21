from rest_framework import serializers
from widok.models import Oceny,Kometarz,Obrazek


class ObrazekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obrazek
        fields = '__all__'

class OcenySerializer(serializers.ModelSerializer):
    class Meta:
        model = Oceny
        fields = '__all__'

class KometarzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kometarz
        fields = '__all__'


