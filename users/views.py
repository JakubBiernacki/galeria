#http
from django.shortcuts import render,redirect
#wiadomość
from django.contrib import messages
#rejestracja
from .form import Register_Form
#logowanie
from django.contrib.auth import authenticate, login,logout

# Create your views here.

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