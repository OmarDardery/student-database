from pydoc_data.topics import topics
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .models import Subject, Sheets, Notes, Semester, Mcq, Topic, Link
from pydantic import BaseModel, Field
from google import genai
from django.conf import settings

client = genai.Client(api_key=settings.GOOGLE_API_KEY)

class mcq_data(BaseModel):
    subject_name: str = Field(..., description="ID of the subject")
    topic_name: str = Field(..., description="ID of the topic")

    mcq_name: str = Field(..., description="The question text")
    mcq_a: str = Field(..., description="Option A text")
    mcq_b: str = Field(..., description="Option B text")
    mcq_c: str = Field(..., description="Option C text")
    mcq_d: str = Field(..., description="Option D text")
    mcq_answer: str = Field(..., description="Correct answer option (A/B/C/D)")
    pending: bool = Field(False, description="Whether the MCQ is pending approval")
    repeated: bool = Field(False, description="Whether the MCQ is repeated or not")

def index(request):
    if request.user.is_authenticated:
        response = redirect('home')
    else:
        response = render(request, 'liasu/permenant static/index.html')
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
    links = list(Link.objects.filter(pending=False).values())
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
        },
        "admin": request.user.is_superuser,
        "links": links
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


from django.core.mail import send_mail
import random
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
            # Check if SENDGRID_API_KEY is set
            if not os.environ.get('SENDGRID_API_KEY'):
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
                return JsonResponse({"requestStatus": "True"})
            except Exception as e:
                return JsonResponse({"requestStatus": "False", "message": f"Failed to send email: {str(e)}"})
                
        except json.JSONDecodeError:
            return JsonResponse({"requestStatus": "False", "message": "Invalid JSON data"})
        except Exception as e:
            return JsonResponse({"requestStatus": "False", "message": f"Error: {str(e)}"})
    else:
        return JsonResponse({"requestStatus": "False", "message": "invalid request method"})


def validate_code(request):
    if request.method == "POST":
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            user_code = data.get("code")
            
            if not request.session.get("code"):
                return JsonResponse({"requestStatus": "False", "message": "No code set"})
            else:
                # Convert both to strings, strip whitespace, and compare
                session_code_str = str(request.session["code"]).strip()
                user_code_str = str(user_code).strip()

                if user_code_str == session_code_str:
                    return JsonResponse({"requestStatus": "True"})
                else:
                    return JsonResponse({"requestStatus": "False", "message": "Invalid code"})
        except json.JSONDecodeError as e:
            return JsonResponse({"requestStatus": "False", "message": "Invalid JSON data"})
        except Exception as e:
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
        mcqs = Mcq.objects.select_related('topic').filter(subject=subject_id, pending=False)
        mcqs_list = []
        for mcq in mcqs:
            mcq_data = {k: v for k, v in vars(mcq).items() if not k.startswith('_') and k != 'topic_id'}
            topic_data = {f"topic_{k}": v for k, v in vars(mcq.topic).items() if not k.startswith('_')}
            mcqs_list.append({**mcq_data, **topic_data})
        topics = []

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

@login_required(login_url='login')
def mcq_view(request):
    subjects = list(Subject.objects.all().values())
    topics = list(Topic.objects.all().values())
    data = {
        "subjects": subjects,
        "topics": topics,
        "context": {
            # ... your existing context ...
            "range18": range(18),
            "range25": range(25),
            "range9": range(9),
            "range2": range(2),
            "range8": range(8),
        }
    }
    return render(request, 'MCQ/add.html', data)

@login_required(login_url='login')
def add_mcq(request):
    if request.method == "POST":
        try:
            subject_id = request.POST.get("subject")
            topic_id = request.POST.get("topic")
            if not subject_id or subject_id == 'undefined' or not topic_id or topic_id == 'undefined':
                return JsonResponse({"status": "error", "message": "Subject and topic must be selected."})
            mcq_name = request.POST.get("question")
            mcq_a = request.POST.get("option1")
            mcq_b = request.POST.get("option2")
            mcq_c = request.POST.get("option3")
            mcq_d = request.POST.get("option4")
            answer_map = {'option1': 'A', 'option2': 'B', 'option3': 'C', 'option4': 'D'}
            mcq_answer = answer_map.get(request.POST.get("answer"), 'A')
            data = {
                "subject_name": Subject.objects.get(id=subject_id).name,
                "topic_name": Topic.objects.get(id=topic_id).topic_name,
                "mcq_name": mcq_name,
                "mcq_a": mcq_a,
                "mcq_b": mcq_b,
                "mcq_c": mcq_c,
                "mcq_d": mcq_d,
                "mcq_answer": mcq_answer,
                "pending": False,
            }
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"You are now an MCQ judge. judge the following mcq. if it has inappropriate content or irrelevant content, return pending to be 'True' otherwise return pending to be 'False'. Also, punctuate and fix typos in the data, additionally, if u find that the mcq is repeated, set 'repeated' to be true the mcq should be deemed repeated if both the question and the answer are similar to another mcq.\n{data}\n\n past mcqs: {list(Mcq.objects.filter(subject_id=subject_id).values())}",
                config={
                    "response_mime_type": "application/json",
                    "response_schema": mcq_data,
                },
            )
            content = response.parsed
            if not content.repeated:
                mcq = Mcq.objects.create(
                    posted_by=request.user,
                    subject_id=subject_id,
                    topic_id=topic_id,
                    mcq_name=content.mcq_name,
                    mcq_a=content.mcq_a,
                    mcq_b=content.mcq_b,
                    mcq_c=content.mcq_c,
                    mcq_d=content.mcq_d,
                    mcq_answer=content.mcq_answer,
                    pending=content.pending
                )
                mcq.save()

            return redirect('home')
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"})
