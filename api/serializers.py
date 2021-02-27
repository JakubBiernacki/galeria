from rest_framework import serializers
from widok.models import Oceny,Kometarz,Obrazek
from users.models import User


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

class UserProfileSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    @classmethod
    def get_img(self,object):
        return object.profile.image.url

    class Meta:
        model = User
        fields = ['id','username','img']


