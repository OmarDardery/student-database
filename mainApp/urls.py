from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="login"),
    path("home", views.home, name="home"),
    path("api/auth", views.authenticate_user, name="authenticate-user"),
    path("api/logout", views.logout_user, name="logout-user"),
    path("api/send-code", views.send_code, name='send-code'),
    path("api/validate-code", views.validate_code, name='validate-code'),
    path("api/sign-up", views.sign_up_user, name='sign-up'),  # Add this line
    path("logout", views.logout_user, name="logout-user"),
    path("mcq/<str:subject_id>", views.mcq, name="mcq"),
]