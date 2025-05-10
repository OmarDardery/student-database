
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, LoginForm



@login_required(login_url='login')
def home(request):
    return render(request, 'mainApp/home.html')

def userlogin(request):
    return render(request, 'mainApp/login.html', {'form': LoginForm()})

def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return redirect('login')

def signup(request):
    return render(request, 'mainApp/signup.html', {'form': StudentRegistrationForm()})

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('index')
    return render(request,"mainApp/signup.html", {'form': StudentRegistrationForm(), "error": "ID is already signed up or password is invalid."})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                # Important: Use form instance with data already filled
                return render(request, 'mainApp/login.html', {
                    'form': form,  # Use the bound form
                    'error': 'Invalid ID or password'
                })
        else:
            # Form validation failed
            return render(request, 'mainApp/login.html', {
                'form': form,  # Use the bound form with errors
                'error': 'Please correct the errors below'
            })
    return render(request, "mainApp/login.html", {'form': LoginForm()})


def logout_view(request):
    logout(request)
    return redirect('login')

def react_test(request):
    return render(request, 'liasu/build/index.html')
