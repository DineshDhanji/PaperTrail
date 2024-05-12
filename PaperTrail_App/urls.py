from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views
from . import api_views
from django.conf import settings
from django.conf.urls.static import static

app_name = "PaperTrail_App"

urlpatterns = [
    # Primary Views
    path("", login_required(views.dashboard), name="dashboard"),
    path("upload_docs/", login_required(views.upload_docs), name="upload_docs"),
    path("view_doc/img/d=<int:doc_id>/", login_required(views.view_doc_img), name="view_doc_img"),
    path("view_doc/pdf/d=<int:doc_id>/", login_required(views.view_doc_pdf), name="view_doc_pdf"),
    # Login & Logout
    path("accounts/login/", views.user_login, name="user_login"),
    path("accounts/logout/", login_required(views.user_logout), name="user_logout"),
    
    # APIs Views
    path("api/get_documents/", login_required(api_views.get_documents), name="get_documents"),
    path("api/get_annotations/<int:doc_id>/", login_required(api_views.get_annotations), name="get_annotations"),
    path("api/create_annotation/", login_required(api_views.create_annotation), name="create_annotation"),
    path("api/update_annotation/", login_required(api_views.update_annotation), name="update_annotation"),
    path("api/delete_annotation/", login_required(api_views.delete_annotation), name="delete_annotation"),
    path("api/delete_docfile/", login_required(api_views.delete_docfile), name="delete_docfile"),
    

]
# Serve static and media files only during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
