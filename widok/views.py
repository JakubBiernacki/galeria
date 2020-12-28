from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Obrazek
from .forms import Add_obrazek,Wybrana_ocena,Dodaj_kometarz



#strona g��wna
def index(request):

    obrazki = Obrazek.objects.all().order_by('-data_publikacji')

    obrazki = zip(obrazki,
                  [x.kometarz_set.count() for x in obrazki],#ilosc kom
                  [x.srednia_ocen() for x in obrazki],#srednia ocen
                  [x.oceny_count() for x in obrazki])#ilo�� ocen

    return render(request, 'galeria/pictures_list.html',{'zdjecia':obrazki})


# Usuwanie
def remove(request,id_obrazka:int):
    get_object_or_404(Obrazek,pk=id_obrazka).delete()
    return redirect('index')



# Dodawanie obrazka
def dodaj(request):
    if request.method == 'POST':
        form = Add_obrazek(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.data_publikacji = timezone.now()
            post.autor = User.objects.get(username=str(request.user.username))
            post.save()
            return redirect('widok_obrazka', id_obrazka=post.pk)
    else:
        form = Add_obrazek
    return render(request, 'galeria/formularz_obrazek.html', {'form': form, 'przycisk': 'Dodaj'})



# edycja
def edit(request,id_obrazka:int):
    obrazek = get_object_or_404(Obrazek,pk=id_obrazka)

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


#szczeg�y
def widok_obrazka(request,id_obrazka:int):
    obrazek = get_object_or_404(Obrazek,pk=id_obrazka)


    if request.method == 'POST':

        ocena = Wybrana_ocena(request.POST)
        kom = Dodaj_kometarz(request.POST)

        if ocena.is_valid():
            if obrazek.czy_ocenil(request.user.id)>=1:
                messages.error(request, "Prosze nie hakować ")
            else:
                ocena = ocena.save(commit=False)
                ocena.autor = request.user
                ocena.obrazek = obrazek
                ocena.save()
                messages.info(request, "Dodano ocene")


            return redirect('widok_obrazka', id_obrazka=obrazek.id)

        elif kom.is_valid():
            kometarz = kom.save(commit=False)

            kometarz.autor = request.user
            kometarz.obrazek_id = id_obrazka

            kometarz.save()

            messages.info(request, "Dodano komentarz")
            return redirect('widok_obrazka', id_obrazka=obrazek.pk)

    else:
        ocena = Wybrana_ocena
        komform = Dodaj_kometarz


    # Kometarze
    kometarze = obrazek.kometarz_set.all().order_by('-data_publikacji')

    ilosc_ocen = obrazek.oceny_count()
    srednia = obrazek.srednia_ocen() if ilosc_ocen!=0 else 'brak'
    if srednia !='brak':
        pelne = int((srednia*2)//2)
        gwiazdki = ([2]*pelne)+([1]*int(srednia*2-pelne*2))
        gwiazdki+= [0]*(5 - len(gwiazdki))

    else:
        gwiazdki=[0]*5
    gwiazdki = ''.join(map(str, gwiazdki))

    return render(request,'galeria/detale_obrazek.html',
                  {'obrazek':obrazek,
                   'ocena': ocena,
                   'kom':komform,
                   'kometarze':kometarze,
                   'ilosc_ocen':ilosc_ocen,
                   'srednia':srednia,
                   'gwiazdki':gwiazdki[:5],
                   'autor':obrazek.autor,
                   'ocenil':obrazek.czy_ocenil(request.user.id) if request.user.id else False

                   }
                  )


