from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = "PaperTrail_App"

urlpatterns = [
    # Primary Views
    path("", login_required(views.dashboard), name="dashboard"),
    path("upload_docs/", login_required(views.upload_docs), name="upload_docs"),
    # Login & Logout
    path("accounts/login/", views.user_login, name="user_login"),
    path("accounts/logout/", login_required(views.user_logout), name="user_logout"),
]
# Serve static and media files only during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
