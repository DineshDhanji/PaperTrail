from django.urls import path
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.conf.urls.static import static

from . import views
from . import api_views

app_name = "PaperTrail_App"

urlpatterns = [
    # Primary Views
    path("", login_required(views.dashboard), name="dashboard"),
    path("shared_docs/", login_required(views.shared_docs), name="shared_docs"),
    path("upload_docs/", login_required(views.upload_docs), name="upload_docs"),
    path(
        "view_doc/img/d=<int:doc_id>/",
        login_required(views.view_doc_img),
        name="view_doc_img",
    ),
    path(
        "view_doc/pdf/d=<int:doc_id>/",
        login_required(views.view_doc_pdf),
        name="view_doc_pdf",
    ),
    path(
        "search_doc/",
        login_required(views.search_doc),
        name="search_doc",
    ),
    # Login & Logout
    path("accounts/login/", views.user_login, name="user_login"),
    path("accounts/logout/", login_required(views.user_logout), name="user_logout"),
    path("accounts/signup/", views.user_signup, name="user_signup"),
    # APIs Views
    path(
        "api/get_documents/",
        login_required(api_views.get_documents),
        name="get_documents",
    ),
    path("api/share_with/", login_required(api_views.share_with), name="share_with"),
    path(
        "api/get_share_docs/",
        login_required(api_views.get_share_docs),
        name="get_share_docs",
    ),
    path(
        "api/get_shared_list/<int:doc_id>/",
        login_required(api_views.get_shared_list),
        name="get_shared_list",
    ),
    path(
        "api/remove_access/",
        login_required(api_views.remove_access),
        name="remove_access",
    ),
    path(
        "api/delete_docfile/",
        login_required(api_views.delete_docfile),
        name="delete_docfile",
    ),
    path(
        "api/get_annotations/<int:doc_id>/",
        login_required(api_views.get_annotations),
        name="get_annotations",
    ),
    path(
        "api/create_annotation/",
        login_required(api_views.create_annotation),
        name="create_annotation",
    ),
    path(
        "api/update_annotation/",
        login_required(api_views.update_annotation),
        name="update_annotation",
    ),
    path(
        "api/delete_annotation/",
        login_required(api_views.delete_annotation),
        name="delete_annotation",
    ),
    path(
        "api/search_query/",
        login_required(api_views.search_query),
        name="search_query",
    ),
]

# Serve static and media files only during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
