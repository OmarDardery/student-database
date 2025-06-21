from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .models import Subject, Sheets, Notes, Semester
def index(request):
    if request.user.is_authenticated:
        response = redirect('home')
    else:
        response = render(request, 'liasu/permenant static/index.html')
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
    subjects = list(Subject.objects.all().values())
    sheets = [
        {
            "id": s.id,
            "subject_id": s.subject_id,
            "sheet_name": s.sheet_name,
            "sheet_file": s.sheet_file.url,  # Convert to URL
            "semester_id": s.semester_id,
            "topic_id": s.topic_id,
        }
        for s in Sheets.objects.all()
    ]
    notes = [
        {
            "id": n.id,
            "subject_id": n.subject_id,
            "note_name": n.note_name,
            "note_file": n.note_file.url,  # Convert to URL
            "semester_id": n.semester_id,
            "topic_id": n.topic_id,
        }
        for n in Notes.objects.all()
    ]
    semesters = list(Semester.objects.all().values())
    data = {
        "subjects": subjects,
        "sheets": sheets,
        "notes": notes,
        "semesters": semesters,
        "context": {
            # ... your existing context ...
            "range18": range(18),
            "range25": range(25),
            "range9": range(9),
            "range2": range(2),
            "range8": range(8),
        }
    }
    return render(request, 'home/index.html', data)

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

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')