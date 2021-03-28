from rest_framework import serializers
from widok.models import Oceny, Kometarz, Obrazek
from users.models import User


class KometarzSerializer(serializers.ModelSerializer):
    autor = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    obrazek = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Kometarz
        fields = '__all__'

    def validate(self, data):
        data['autor'] = self.context['request'].user
        data['obrazek'] = Obrazek.objects.get(pk=self.context['id'])
        return data


class OcenySerializer(serializers.ModelSerializer):
    autor = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    obrazek = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Oceny
        fields = '__all__'

    def validate(self, data):
        autor = self.context['request'].user
        obrazek = Obrazek.objects.get(pk=self.context['id'])

        if obrazek.oceny_set.filter(autor=autor).exists():
            raise serializers.ValidationError({"autor": f"Obrazek: {obrazek} został już oceniony przez użytkownika: {autor}"})

        data['autor'] = autor
        data['obrazek'] = obrazek

        return data


class UserProfileSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    @classmethod
    def get_img(self, object):
        return object.profile.image.url

    class Meta:
        model = User
        fields = ['id', 'username', 'img']
