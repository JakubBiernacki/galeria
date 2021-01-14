#http
from django.shortcuts import render,redirect
#wiadomość
from django.contrib import messages
#formularze
from .form import Register_Form,UserUpdateForm,ProfileUpdateForm
#logowanie
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import os

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
