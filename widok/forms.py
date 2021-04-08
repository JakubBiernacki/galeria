from django import forms
from .models import Obrazek, Oceny, Kometarz
from django.contrib.auth.models import User


class Add_obrazek_link(forms.ModelForm):
    class Meta:
        model = Obrazek
        fields = ['obrazek_path', 'tytul']
        widgets = {
            'obrazek_path': forms.TextInput(attrs={'class': 'form-control col-md-12', 'placeholder': 'https://...'}),
            'tytul': forms.TextInput(attrs={'class': 'col-12 col-md-7 col-lg-6 form-control'})
        }


class Add_obrazek_file(forms.ModelForm):
    class Meta:
        model = Obrazek
        fields = ['obrazek_file', 'tytul']
        widgets = {

            'tytul': forms.TextInput(attrs={'class': 'col-12 col-md-7 col-lg-6 form-control'})
        }


