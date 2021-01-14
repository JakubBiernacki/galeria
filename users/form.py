from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class Register_Form(UserCreationForm):
    email = forms.EmailField(help_text = "<b class='text-danger'>ważne </b>Podanie adresu email pomoże w odzyskaniu konta oraz kontakcie")
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists() or '@jbiernacki.pl' in email:
            raise ValidationError("Intnieje użytkownik o takim emailu")
        return self.cleaned_data


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(help_text = "<b class='text-danger'>ważne </b>Podanie adresu email pomoże w odzyskaniu konta oraz kontakcie")
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']




class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields=['image']

