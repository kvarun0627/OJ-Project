from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import registerForm,LoginForm
from django.contrib import messages
from django.contrib.auth import logout as auth_logout

def home(request):
    return render(request,'users/home.html')

def register(request):
    if request.method == 'POST':
        form=registerForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            request.session['username'] = username  #to keep track of user in every page
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = registerForm()
    
    return render(request, 'users/register.html', {'form': form})

def login(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            messages.success(request, f'{username} Logged In successfully!')
            return redirect('home')
    else:
        form=LoginForm()

    return render(request,'users/login.html',{'form':form})

def logout(request):
    request.session.flush()
    auth_logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')