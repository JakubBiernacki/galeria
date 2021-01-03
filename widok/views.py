from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Obrazek
from .forms import Add_obrazek,Wybrana_ocena,Dodaj_kometarz

from math import floor



#strona g��wna
def index(request):

    obrazki = Obrazek.objects.all().order_by('-data_publikacji')

    return render(request, 'galeria/pictures_list.html',{'obrazki':obrazki})


# Usuwanie
@login_required
def remove(request,id_obrazka:int):
    obrazek = get_object_or_404(Obrazek, pk=id_obrazka)
    if request.user == obrazek.autor or request.user.is_superuser:
        messages.info(request, f"Obrazek {obrazek.tytul} został poprawnie usunięty")
        obrazek.delete()
        return redirect('index')

    else:
        messages.error(request, "Nie masz uprawnień do tej operacji")


    return redirect('widok_obrazka',id_obrazka = obrazek.id)



# Dodawanie obrazka
@login_required
def dodaj(request):
    if request.method == 'POST':
        form = Add_obrazek(request.POST)

        if form.is_valid():
            post = form.save(commit=False)

            if post.obrazek_path.startswith('https://') and post.obrazek_path.endswith(('.jpg','.png','.jpeg')):
                post.data_publikacji = timezone.now()
                post.autor = User.objects.get(username=str(request.user.username))
                post.save()
                return redirect('widok_obrazka', id_obrazka=post.pk)
            else:
                messages.error(request, "Link jest niepoprawny lub niebezpieczny")
                return render(request, 'galeria/formularz_obrazek.html', {'form': form, 'przycisk': 'Dodaj'})

    else:
        form = Add_obrazek
    return render(request, 'galeria/formularz_obrazek.html', {'form': form, 'przycisk': 'Dodaj'})



# edycja
@login_required
def edit(request,id_obrazka:int):
    obrazek = get_object_or_404(Obrazek,pk=id_obrazka)
    if request.user == obrazek.autor or request.user.is_superuser:

        if request.method == 'POST':
            form = Add_obrazek(request.POST, instance=obrazek)  # wprowadza istniejace dane

            if form.is_valid():
                obrazek = form.save(commit=False)
                obrazek.data_publikacji = timezone.now()
                obrazek.save()
                return redirect('widok_obrazka', id_obrazka=obrazek.id)
        else:
            form =  Add_obrazek(instance=obrazek )
        return render(request, 'galeria/formularz_obrazek.html', {'form': form, 'przycisk': 'edytuj post','obrazek': obrazek })
    else:
        messages.error(request, "Nie masz uprawnień do tej operacji")
        return redirect('widok_obrazka', id_obrazka=obrazek.id)



#szczeg�y
def widok_obrazka(request,id_obrazka:int):
    obrazek = get_object_or_404(Obrazek,pk=id_obrazka)


    if request.method == 'POST':

        formocena = Wybrana_ocena(request.POST)
        formkom = Dodaj_kometarz(request.POST)
        #ocena
        if formocena.is_valid():
            if obrazek.czy_ocenil(request.user.id)>=1:
                messages.error(request, "Prosze nie hakować ")
            else:
                ocena = formocena.save(commit=False)

                ocena.autor = request.user
                ocena.obrazek = obrazek

                ocena.save()
                messages.info(request, "Dodano ocene")


            return redirect('widok_obrazka', id_obrazka=obrazek.id)

        #komentarz
        elif formkom.is_valid():
            kometarz = formkom.save(commit=False)

            kometarz.autor = request.user
            kometarz.obrazek_id = id_obrazka

            kometarz.save()

            messages.info(request, "Dodano komentarz")
            return redirect('widok_obrazka', id_obrazka=obrazek.pk)

    else:
        formocena = Wybrana_ocena
        formkom = Dodaj_kometarz



    kometarze = obrazek.kometarz_set.all().order_by('-data_publikacji')

    #ile gwiazdek narysować
    srednia = obrazek.srednia_ocen() if obrazek.oceny_count() else False
    if srednia:
        pelne = floor(srednia)
        gwiazdki = [2]*pelne +[1] if srednia-pelne else [2]*pelne
        gwiazdki+= [0]*(5 - len(gwiazdki))

    else:
        gwiazdki=[0]*5

    czy_ocenil = obrazek.czy_ocenil(request.user.id) if request.user.id else False

    obrazek_dane = {
                   'obrazek':obrazek,
                   'formocena': formocena,
                   'formkom':formkom,
                   'kometarze':kometarze,
                   'gwiazdki':gwiazdki,
                   'czy_ocenil': czy_ocenil,
                   }


    return render(request,'galeria/detale_obrazek.html',obrazek_dane)


