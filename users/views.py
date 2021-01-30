#http
from django.shortcuts import render,redirect
#wiadomość
from django.contrib import messages
#formularze
from .form import Register_Form,UserUpdateForm,ProfileUpdateForm,ContactForm
#logowanie
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import os

from django.core.mail import send_mail
from django.conf import settings

def rejestracja(request):

    if request.method == 'POST':
        form = Register_Form(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(request,f"Witaj \"{str(username).capitalize()}\"twoje konto zostało poprawnie utworzone")
            #logowanie
            new_user = authenticate(username=username,password=form.cleaned_data['password1'],)

            login(request, new_user)

            return redirect('index')
    else:
        form = Register_Form()
    return render(request,'users/register.html',{'form':form})

def logout_user(request):
    logout(request)
    messages.success(request,"Zostałeś poprawnie wylogowany")
    return redirect('index')




@login_required
def profile(request):
    if request.method == 'POST':

        curent_user = request.user
        old_email = curent_user.email
        old_img = curent_user.profile.image

        u_form = UserUpdateForm(request.POST,instance=curent_user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=curent_user.profile)

        if u_form.is_valid() and p_form.is_valid():
            nowy_email = u_form.cleaned_data.get('email')
            if (nowy_email != old_email and User.objects.filter(email=nowy_email).exists()) or '@jbiernacki.pl' in nowy_email:
                messages.error(request,'istnieje już użytkownik o podanym mailu')
                return redirect('profile')

            #tak na wszeli wypadek xd
            if nowy_email==old_email or not User.objects.filter(email=nowy_email).exists():
                u_form.save()

            p_form.save()

            if len(request.FILES) !=0 and old_img.url != '/media/default.jpg':
                os.remove(old_img.path)

            messages.success(request, 'Twoje konto zostało uaktualnione!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }



    return render(request,'users/profile.html',context)

@login_required
def contact(request):
    if request.method == 'POST':

        form = ContactForm(request.POST)
        if form.is_valid():

            subject = form.cleaned_data['tytul']
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['tresc']
            try:
                send_mail(f"User: {request.user.username} Tytuł: "+subject, message, from_email, [getattr(settings,"EMAIL_HOST_USER")])
                messages.success(request, "Wiadomość została wysłana")
                if form.cleaned_data['checkbox']:
                    send_mail("Tytuł: " + subject, 'To jest wysłana przez ciebie wiadomość przez strone https://galeria.jbiernacki.pl/ : \n\n'+message, 'Galeria',[from_email])
                return redirect('index')
            except:
                messages.error(request, "Wiadomość nie zostałą wysłana!")

    form = ContactForm()

    form.initial['email'] = request.user.email if request.user.email else ''
    return render(request, 'users/contact.html', {'form': form})
