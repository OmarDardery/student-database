from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .models import Subject, Sheets, Notes, Semester, Mcq
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
    print(data)
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


from django.core.mail import send_mail
import random
import logging
import os

def send_code(request):
    if request.method == "POST":
        try:
            # Parse JSON data
            data = json.loads(request.body)
            user_id = data.get('id')  # This is the student ID
            
            if not user_id:
                return JsonResponse({"requestStatus": "False", "message": "Student ID is required"})
            
            # Generate a random 6-digit code
            code = str(random.randint(100000, 999999))
            
            # Store the code in the session
            request.session["code"] = code
            request.session.modified = True
            
            # Construct the email address from ID
            email = f"{user_id}@students.eui.edu.eg"
            
            # Log for debugging
            logging.warning(f"Attempting to send verification code {code} to {email}")
            
            # Check if SENDGRID_API_KEY is set
            if not os.environ.get('SENDGRID_API_KEY'):
                logging.error("SENDGRID_API_KEY is not set in environment variables")
                return JsonResponse({"requestStatus": "False", "message": "Email configuration error"})
            
            # Send the email with the code
            try:
                send_mail(
                    subject="Your Student Database Verification Code",
                    message=f"Your verification code is: {code}\n\nPlease enter this code in the verification page to complete your registration.",
                    from_email="oadardery@gmail.com",  # Update with your verified sender
                    recipient_list=[email],
                    fail_silently=False,
                )
                logging.warning(f"Email sent successfully to {email}")
                return JsonResponse({"requestStatus": "True"})
            except Exception as e:
                logging.error(f"Failed to send email: {str(e)}")
                return JsonResponse({"requestStatus": "False", "message": f"Failed to send email: {str(e)}"})
                
        except json.JSONDecodeError:
            return JsonResponse({"requestStatus": "False", "message": "Invalid JSON data"})
        except Exception as e:
            logging.error(f"Error in send_code: {str(e)}")
            return JsonResponse({"requestStatus": "False", "message": f"Error: {str(e)}"})
    else:
        return JsonResponse({"requestStatus": "False", "message": "invalid request method"})

import json
import logging

def validate_code(request):
    if request.method == "POST":
        try:
            # Log the session data
            logging.warning(f"Session code: '{request.session.get('code')}'")
            logging.warning(f"Session keys: {list(request.session.keys())}")
            
            # Parse JSON data from request body
            data = json.loads(request.body)
            logging.warning(f"Received data: {data}")
            user_code = data.get("code")  # Get 'code' from JSON data
            logging.warning(f"Received user_code: '{user_code}'")
            
            if not request.session.get("code"):
                return JsonResponse({"requestStatus": "False", "message": "No code set"})
            else:
                # Convert both to strings, strip whitespace, and compare
                session_code_str = str(request.session["code"]).strip()
                user_code_str = str(user_code).strip()
                
                logging.warning(f"Comparing: '{user_code_str}' (type: {type(user_code_str)}) with '{session_code_str}' (type: {type(session_code_str)})")
                logging.warning(f"String representation equality: {user_code_str == session_code_str}")
                
                if user_code_str == session_code_str:
                    return JsonResponse({"requestStatus": "True"})
                else:
                    # Log the comparison with repr to see hidden characters
                    logging.warning(f"Code comparison failed: {repr(user_code_str)} != {repr(session_code_str)}")
                    # Check character by character
                    if len(user_code_str) == len(session_code_str):
                        for i, (c1, c2) in enumerate(zip(user_code_str, session_code_str)):
                            if c1 != c2:
                                logging.warning(f"Mismatch at position {i}: '{c1}' (ord: {ord(c1)}) != '{c2}' (ord: {ord(c2)})")
                    
                    return JsonResponse({"requestStatus": "False", "message": "Invalid code"})
        except json.JSONDecodeError as e:
            logging.error(f"JSON Decode Error: {str(e)}")
            return JsonResponse({"requestStatus": "False", "message": "Invalid JSON data"})
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return JsonResponse({"requestStatus": "False", "message": f"Server error: {str(e)}"})
    else:
        return JsonResponse({"requestStatus": "False", "message": "invalid request method"})

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

def sign_up_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("userId")
            user_password = data.get("userPassword")
            
            # Create the user using Django's User model
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            # Check if user already exists
            if User.objects.filter(username=user_id).exists():
                return JsonResponse({"completed": False, "message": "User already exists"})
            
            # Create the user
            user = User.objects.create_user(username=user_id, password=user_password)
            user.save()
            
            # Log the user in
            login(request, user)
            
            return JsonResponse({"completed": True})
        except Exception as e:
            print(f"Error in sign_up_user: {str(e)}")
            return JsonResponse({"completed": False, "message": str(e)})
    else:
        return JsonResponse({"completed": False, "message": "Invalid request method"})

@login_required(login_url='login')
def mcq(request, subject_id):
    try:
        mcqs = Mcq.objects.select_related('topic').filter(subject=subject_id)
        mcqs_list = []
        for mcq in mcqs:
            mcq_data = {k: v for k, v in vars(mcq).items() if not k.startswith('_') and k != 'topic_id'}
            topic_data = {f"topic_{k}": v for k, v in vars(mcq.topic).items() if not k.startswith('_')}
            mcqs_list.append({**mcq_data, **topic_data})
        topics = []
        print("mcqs_list", mcqs_list)

        for mcq in mcqs_list:
            if {"name": mcq["topic_topic_name"], "id": mcq["topic_id"]} not in topics:
                topics.append({"name": mcq["topic_topic_name"], "id": mcq["topic_id"]})

        return render(request, 'MCQ/index.html', {'mcqs': mcqs_list, "topics": topics, "context": {
                    "range18": range(18),
                    "range25": range(25),
                    "range9": range(9),
                    "range2": range(2),
                    "range8": range(8),
                }})
    except Mcq.DoesNotExist:
        return JsonResponse({"error": "mcq not found"}, status=404)