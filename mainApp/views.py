from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
def index(request):
    if request.user.is_authenticated:
        response = redirect('home')
    else:
        response = render(request, 'liasu/build/index.html')
    response.set_cookie(
        "student_database_csrftoken",
        request.COOKIES.get("csrftoken"),
        httponly=False,
        samesite='Lax',
        secure=request.is_secure(),
    )
    return response

@login_required(login_url='login')
def home(request):
    return render(request, 'home/build/index.html')

def authenticate_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('id')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"authenticated": "True"})
        else:
            return JsonResponse({"authenticated": "False", "message": "Invalid credentials"})
    else:
        return JsonResponse({"authenticated": "False", "message": "Invalid request method"})

@login_required(login_url='')
def logout_user(request):
    if request.method == 'POST':
        print("reached")
        logout(request)
        return JsonResponse({"logged_out": "True"})
    else:
        return JsonResponse({"logged_out": "False", "message": "Invalid request method"})

def send_code(request):
    if request.method == "POST":
        request.session["code"] = 123456
        return JsonResponse({"requestStatus": "True"})
    else:
        return JsonResponse({"requestStatus": "False", "message": "invalid request method"})

def validate_code(request):
    if request.method == "POST":
        if not request.session["code"]:
            return JsonResponse({"requestStatus": "False", "message": "No code set"})
        else:
            if request.POST.get("code") == request.session["code"]:
                return JsonResponse({"requestStatus": "True"})
            else:
                return JsonResponse({"requestStatus": "False", "message": "Invalid code"})
    else:
        return JsonResponse({"requestStatus": "False", "message": "invalid request method"})