from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
    path("api/auth", views.authenticate_user, name="authenticate-user"),
    path("api/logout", views.logout_user, name="logout-user"),
    path("api/send-code", views.send_code, name='send-code'),
    path("api/validate-code", views.validate_code, name='validate-code'),
]