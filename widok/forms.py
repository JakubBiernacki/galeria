from django import forms
from .models import Obrazek,Oceny,Kometarz

class Add_obrazek_link(forms.ModelForm):

    class Meta:
        model = Obrazek
        fields = ['obrazek_path','tytul']
        widgets ={
            'obrazek_path':forms.TextInput(attrs={'class':'form-control col-md-12','placeholder':'https://...'}),
            'tytul':forms.TextInput(attrs={'class':'col-12 col-md-7 col-lg-6 form-control'})
        }

class Add_obrazek_file(forms.ModelForm):
    class Meta:
        model = Obrazek
        fields = ['obrazek_file','tytul']
        widgets ={

            'tytul':forms.TextInput(attrs={'class':'col-12 col-md-7 col-lg-6 form-control'})
        }


WARTOSCI_OCEN = [(str(x),'') for x in range(5,0,-1)]
class Wybrana_ocena(forms.ModelForm):

    ocena = forms.ChoiceField(widget=forms.RadioSelect(),choices=WARTOSCI_OCEN)
    class Meta:
        model = Oceny
        fields = ['ocena']




class Dodaj_kometarz(forms.ModelForm):
    class Meta:
        model = Kometarz
        fields = ['tresc']
        widgets = {

            'tresc': forms.Textarea(attrs={'class': 'col-11 form-control','rows':'3','placeholder':'twój komentarz...'})
        }



