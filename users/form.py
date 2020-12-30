from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm

class Register_Form(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','password1','password2',]

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(help_text = "<b class='text-danger'>ważne </b>Podanie adresu email pomoże w odzyskaniu konta oraz kontakcie<br>(jeżeli będzie mi się chciało go zrobić)<br>"
                                         " poza tym jest niezbędny do zmiany zdjęcia profilowego<br>(jeżeli chcesz zmienić zdjęcie nie podając adresu wpisz <u>test@email.com</u>)")
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']



class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields=['image']