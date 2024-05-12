from django.contrib import admin
from django.urls import path, include

from django.urls import re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("PaperTrail_App.urls")),
    # your other paths here
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]
handler404 = "PaperTrail_App.views.page_not_found_404"
