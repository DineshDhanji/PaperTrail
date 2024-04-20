from django.urls import path
from . import views

app_name = "PaperTrail_App"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]
