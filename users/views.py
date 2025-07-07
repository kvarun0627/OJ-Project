from django.shortcuts import render, redirect
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from django.contrib.auth import logout as auth_logout , login as auth_login
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            messages.success(request, f'Account created for {user.username}!')
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

def login(request):
    if request.method =='POST':
        form=LoginForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            auth_login(request , user)
            messages.success(request, f'{user.username} Logged In successfully!')
            return redirect('question_list')
        else:
            print("login error :", form.errors)
            messages.error(request,"Invalid credentials")
    else:
        form=LoginForm()

    return render(request,'users/login.html',{'form':form})

def logout(request):
    request.session.flush()
    auth_logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('question_list')