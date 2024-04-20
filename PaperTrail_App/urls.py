from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = "PaperTrail_App"

urlpatterns = [
    # Primary Views
    path("", login_required(views.dashboard), name="dashboard"),
    # Login & Logout
    path("accounts/login/", views.user_login, name="user_login"),
    path("accounts/logout/", login_required(views.user_logout), name="user_logout"),
]
