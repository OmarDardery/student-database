from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.userlogin, name="login"),
    path("login-view", views.login_view, name="login-view"),
    path("logout", views.logout, name="logout"),
    path("signup", views.signup, name="signup"),
    path("register", views.register, name="register"),
    path("home", views.home, name="home"),
    path("react", views.react_test, name="react"),
    path("api/validate/<str:id>/", views.validate_and_send_code, name="validate_student_id"),
]