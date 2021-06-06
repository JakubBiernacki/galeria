from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Obrazek
from .forms import Add_obrazek_link, Add_obrazek_file
from .utils import link_check

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DeleteView,DetailView,View


from django.contrib.auth.models import User

from django.core.cache import cache



# główny widok
ilosc_obrazkow_na_strone = 9


class PhotoListView(ListView):
    model = Obrazek
    template_name = 'widok/home.html'
    paginate_by = ilosc_obrazkow_na_strone

    def get_queryset(self):
        queryset = Obrazek.objects.all().prefetch_related('kometarz_set', 'oceny_set').order_by('-data_publikacji')

        return cache.get_or_set('obrazy', queryset, 500)
        # return queryset

# lista uzytkownika

class UserPostView(ListView):
    model = Obrazek
    template_name = 'widok/home.html'

    paginate_by = ilosc_obrazkow_na_strone

    def get_queryset(self):
        user = get_object_or_404(User.objects.select_related('profile'), username=self.kwargs.get('username'))
        self.kwargs['img'] = user.profile.image.url
        queryset = Obrazek.objects.filter(autor=user).order_by('-data_publikacji').prefetch_related('kometarz_set',
                                                                                                    'oceny_set')
        return cache.get_or_set(f'obrazy_user{user.id}', queryset, 100)
        # return queryset


# Usuwanie
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Obrazek
    success_url = '/'

    def test_func(self):
        obrazek = self.get_object()
        return self.request.user == obrazek.autor or self.request.user.is_superuser



# Dodawanie obrazka
@login_required
def add(request, opcja):
    if request.method == 'POST':

        form = Add_obrazek_link(request.POST) if opcja == 'link' else Add_obrazek_file(request.POST, request.FILES)

        if form.is_valid():
            obrazek = form.save(commit=False)

            link_ok = link_check(obrazek.obrazek_path) if opcja == 'link' else [True]

            if link_ok[0]:

                obrazek.data_publikacji = timezone.now()
                obrazek.autor = request.user

                obrazek.save()

                return redirect("detail", pk=obrazek.pk)
            else:
                messages.error(request, link_ok[1])
                return render(request, 'widok/form.html', {'form': form, 'przycisk': 'Dodaj', 'opcja': opcja})

    else:
        form = Add_obrazek_link if opcja == 'link' else Add_obrazek_file
    return render(request, 'widok/form.html', {'form': form, 'przycisk': 'Dodaj', 'opcja': opcja})


# edycja
@login_required
def edit(request, id_obrazka: int):
    obrazek = get_object_or_404(Obrazek, pk=id_obrazka)
    old_path = obrazek.obrazek_path

    if request.user == obrazek.autor or request.user.is_superuser:

        if request.method == 'POST':

            form = Add_obrazek_link(request.POST, instance=obrazek) if obrazek.obrazek_path else Add_obrazek_file(
                request.POST, request.FILES, instance=obrazek)  # wprowadza istniejace dane

            if form.is_valid():
                link_ok = link_check(obrazek.obrazek_path) if obrazek.obrazek_path else [True]
                if link_ok[0]:

                    obrazek = form.save(commit=False)

                    obrazek.data_publikacji = timezone.now()
                    obrazek.save()

                    if obrazek.obrazek_path != old_path:
                        obrazek.oceny_set.all().delete()

                    return redirect('detail', pk=obrazek.id)
                else:
                    messages.error(request, link_ok[1])
                    return redirect('edit', pk=obrazek.id)

        else:
            form = Add_obrazek_link(instance=obrazek) if obrazek.obrazek_path else Add_obrazek_file(instance=obrazek)

        return render(request, 'widok/form.html', {'form': form, 'przycisk': 'edytuj post', 'obrazek': obrazek})

    else:
        messages.error(request, "Nie masz uprawnień do tej operacji")
        return redirect('detail', pk=obrazek.id)




class ObrazekDetailView(DetailView):
    queryset = Obrazek.objects.select_related('autor', 'autor__profile')
    template_name = 'widok/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        czy_ocenil = 0
        if user.id:
            if ocena := self.object.oceny_set.filter(autor=user):
                czy_ocenil = ocena[0].ocena

        context['czy_ocenil'] = czy_ocenil
        context['podglad_gwiazdek'] = [5, 4, 3, 2, 1]
        return context




