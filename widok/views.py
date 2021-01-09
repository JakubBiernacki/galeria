from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Obrazek
from .forms import Add_obrazek,Wybrana_ocena,Dodaj_kometarz

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DeleteView





def link_check(path):
    from PIL import Image
    import requests
    from io import BytesIO

    if path.startswith('https://') and path.endswith(('.jpg', '.png', '.jpeg')):
        try:
            response = requests.get(path)
            img = Image.open(BytesIO(response.content))

        except:
            error = "Nie można pobrać obrazu (link jest niepoprawny)"
            return False, error
        w, h = img.size
        if w >= 640 and h >= 480:
            return True,False
        else:
            error = 'obraz ma za niską rozdzielczość (min 640x480px)'


    else:
        error = "Link jest niepoprawny lub niebezpieczny"

    return False, error

ilosc_obrazkow_na_strone = 9

#główny widok
class PhotoListView(ListView):
    model = Obrazek
    template_name = 'widok/home.html'
    ordering = ['-data_publikacji']
    paginate_by = ilosc_obrazkow_na_strone


# Usuwanie
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Obrazek
    success_url = '/'

    def test_func(self):
        obrazek = self.get_object()
        if self.request.user == obrazek.autor or self.request.user.is_superuser:
            return True
        return False




# Dodawanie obrazka
@login_required
def add(request):
    if request.method == 'POST':
        form = Add_obrazek(request.POST)

        if form.is_valid():
            obrazek = form.save(commit=False)

            link_ok = link_check(obrazek.obrazek_path)

            if link_ok[0]:

                obrazek.data_publikacji = timezone.now()
                obrazek.autor = request.user
                obrazek.save()
                return redirect("detail", id_obrazka=obrazek.pk)
            else:
                messages.error(request, link_ok[1])
                return render(request, 'widok/form.html', {'form': form, 'przycisk': 'Dodaj'})

    else:
        form = Add_obrazek
    return render(request, 'widok/form.html', {'form': form, 'przycisk': 'Dodaj'})



# edycja
@login_required
def edit(request,id_obrazka:int):
    obrazek = get_object_or_404(Obrazek,pk=id_obrazka)
    old_path = obrazek.obrazek_path
    if request.user == obrazek.autor or request.user.is_superuser:

        if request.method == 'POST':
            form = Add_obrazek(request.POST, instance=obrazek)  # wprowadza istniejace dane

            if form.is_valid():
                link_ok = link_check(obrazek.obrazek_path)
                if link_ok[0]:

                    obrazek = form.save(commit=False)
                    obrazek.data_publikacji = timezone.now()
                    obrazek.save()
                    if obrazek.obrazek_path != old_path:

                        obrazek.oceny_set.all().delete()

                    return redirect('detail', id_obrazka=obrazek.id)
                else:
                    messages.error(request, link_ok[1])
                    return redirect('edit',id_obrazka = obrazek.id)

        else:
            form =  Add_obrazek(instance=obrazek )

        return render(request, 'widok/form.html', {'form': form, 'przycisk': 'edytuj post','obrazek': obrazek })

    else:
        messages.error(request, "Nie masz uprawnień do tej operacji")
        return redirect('detail', id_obrazka=obrazek.id)




def detail(request,id_obrazka:int):
    obrazek = get_object_or_404(Obrazek,pk=id_obrazka)


    if request.method == 'POST':

        form_ocena = Wybrana_ocena(request.POST)
        form_kom = Dodaj_kometarz(request.POST)
        #ocena
        if form_ocena.is_valid():
            if obrazek.czy_ocenil(request.user.id):
                messages.error(request, "Prosze nie hakować ")
            else:
                ocena = form_ocena.save(commit=False)

                ocena.autor = request.user
                ocena.obrazek = obrazek

                ocena.save()
                messages.info(request, "Dodano ocene")


            return redirect('detail', id_obrazka=obrazek.id)

        #komentarz
        elif form_kom.is_valid():
            kometarz = form_kom.save(commit=False)

            kometarz.autor = request.user
            kometarz.obrazek_id = id_obrazka

            kometarz.save()

            messages.info(request, "Dodano komentarz")
            return redirect('detail', id_obrazka=obrazek.pk)

    else:
        form_ocena = Wybrana_ocena
        form_kom = Dodaj_kometarz



    kometarze = obrazek.kometarz_set.all().order_by('-data_publikacji')

    #ile gwiazdek narysować
    srednia = obrazek.srednia_ocen() if obrazek.oceny_count() else False
    if srednia:
        pelne = int(srednia)
        gwiazdki = [2]*pelne +[1] if srednia-pelne else [2]*pelne
        gwiazdki+= [0]*(5 - len(gwiazdki))

    else:
        gwiazdki=[0]*5

    czy_ocenil = obrazek.czy_ocenil(request.user.id) if request.user.id else False

    #cofinij do





    obrazek_dane = {
                   'obrazek':obrazek,
                   'formocena': form_ocena,
                   'formkom':form_kom,
                   'kometarze':kometarze,
                   'gwiazdki':gwiazdki,
                   'czy_ocenil': czy_ocenil,
                    'podglad_gwiazdek': [5,4,3,2,1],

                   }


    return render(request,'widok/detail.html',obrazek_dane)





