
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .forms import StudentRegistrationForm, LoginForm
from .models import Student
import os
from django.core.cache import cache

# Generate code

@login_required(login_url='login')
def home(request):
    return render(request, 'mainApp/home.html')

def userlogin(request):
    return render(request, 'mainApp/login.html', {'form': LoginForm()})

def index(request):
    return render(request, "liasu/build/index.html")

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





#api for react

from django.http import JsonResponse
import random
import string
from django.core.mail import send_mail
from django.conf import settings

def authenticate_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'status': 'success', 'message': 'Login successful'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})


import random
import string
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings


def generate_verification_code():
    """Generate a random 6-digit verification code"""
    return ''.join(random.choices(string.digits, k=6))

@csrf_exempt
def validate_and_send_code(request, id):
    if request.method == 'GET':
        # Get the ID from the query parameters
        university_id = id

        if not university_id:
            return JsonResponse({
                'status': 'error',
                'message': 'University ID is required'
            })

        # Basic validation for ID (length check)
        if len(university_id) > 9:
            return JsonResponse({
                'status': 'error',
                'message': 'University ID cannot exceed 9 characters'
            })

        # Check if the ID already exists in the database
        if Student.objects.filter(username=university_id).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'This university ID is already registered'
            })

        # ID is available, generate verification code
        verification_code = generate_verification_code()
        cache_key = f'verification_code_{university_id}'
        cache.set(cache_key, verification_code, timeout=600)  # 600 seconds = 10 minutes

        # Generate email from the ID based on your Student model's pattern
        email = f"{university_id}@students.eui.edu.eg"

        # Send verification email
        try:
            send_mail(
                'Verify Your University Account',
                f'Your verification code is: {verification_code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            # Return success response with email sent confirmation and the code
            return JsonResponse({
                'status': 'success',
                'message': 'ID is available and verification code sent',
            })

        except Exception as e:
            # Log the error but provide a generic message to the user
            print(f"Email sending failed: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to send verification email',
            })

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })

def validate_code(request):
    university_id = request.GET.get('id')
    submitted_code = request.GET.get('code')

    cache_key = f'verification_code_{university_id}'
    stored_code = cache.get(cache_key)

    if stored_code == submitted_code:
        # Optional: delete the code after successful validation
        cache.delete(cache_key)
        return JsonResponse({'status': 'success', 'message': 'Code is valid'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid or expired code'})