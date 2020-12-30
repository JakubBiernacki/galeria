#http
from django.shortcuts import render,redirect
#wiadomość
from django.contrib import messages
#formularze
from .form import Register_Form,UserUpdateForm,ProfileUpdateForm
#logowanie
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

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
        old_img = request.user.profile.image

        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():

            if len(request.FILES) !=0 and old_img.url != '/media/default.jpg':
                os.remove(old_img.path)


            u_form.save()
            p_form.save()
            messages.success(request, f'Your accont has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request,'users/profile.html',context)
