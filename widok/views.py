from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Obrazek
from .forms import Add_obrazek_link,Add_obrazek_file

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DeleteView

from django.contrib.auth.models import User

#wysyłanie maila





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

    paginate_by = ilosc_obrazkow_na_strone

    def get_queryset(self):
        queryset = Obrazek.objects.all().prefetch_related('kometarz_set','oceny_set').order_by('-data_publikacji')
        return queryset

#lista uzytkownika

class UserPostView(ListView):
    model = Obrazek
    template_name = 'widok/home.html'


    paginate_by = ilosc_obrazkow_na_strone

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))


        self.kwargs['img'] = user.profile.image.url
        return  Obrazek.objects.filter(autor = user).order_by('-data_publikacji').prefetch_related('kometarz_set','oceny_set')

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
def add(request,opcja):
    if request.method == 'POST':

        form = Add_obrazek_link(request.POST) if opcja=='link' else  Add_obrazek_file(request.POST,request.FILES)

        if form.is_valid():
            obrazek = form.save(commit=False)


            link_ok = link_check(obrazek.obrazek_path) if opcja=='link' else [True]

            if link_ok[0]:


                obrazek.data_publikacji = timezone.now()
                obrazek.autor = request.user



                obrazek.save()


                return redirect("detail", id_obrazka=obrazek.pk)
            else:
                messages.error(request, link_ok[1])
                return render(request, 'widok/form.html', {'form': form, 'przycisk': 'Dodaj','opcja':opcja})

    else:
        form = Add_obrazek_link if opcja=='link' else  Add_obrazek_file
    return render(request, 'widok/form.html', {'form': form, 'przycisk': 'Dodaj','opcja':opcja})



# edycja
@login_required
def edit(request,id_obrazka:int):
    obrazek = get_object_or_404(Obrazek,pk=id_obrazka)
    old_path = obrazek.obrazek_path

    if request.user == obrazek.autor or request.user.is_superuser:

        if request.method == 'POST':

            form = Add_obrazek_link(request.POST, instance=obrazek) if obrazek.obrazek_path else Add_obrazek_file(request.POST,request.FILES, instance=obrazek)  # wprowadza istniejace dane

            if form.is_valid():
                link_ok = link_check(obrazek.obrazek_path) if obrazek.obrazek_path else [True]
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
            form =  Add_obrazek_link(instance=obrazek) if obrazek.obrazek_path else Add_obrazek_file(instance=obrazek)

        return render(request, 'widok/form.html', {'form': form, 'przycisk': 'edytuj post','obrazek': obrazek })

    else:
        messages.error(request, "Nie masz uprawnień do tej operacji")
        return redirect('detail', id_obrazka=obrazek.id)




def detail(request,id_obrazka:int):
    obrazek = get_object_or_404(Obrazek,pk=id_obrazka)
    czy_ocenil = obrazek.czy_ocenil(request.user.id) if request.user.id else False

    obrazek_dane = {
        'obrazek':obrazek,
        'czy_ocenil': czy_ocenil,
        'podglad_gwiazdek': [5,4,3,2,1],
        }


    return render(request,'widok/detail.html',obrazek_dane)

#kontakt





