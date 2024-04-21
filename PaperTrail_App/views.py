from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import UserLoginForm, DocumentForm
from .models import Document


def user_login(request):
    if request.user.is_authenticated:
        return redirect("PaperTrail_App:dashboard")

    login_form = UserLoginForm()

    if request.method == "POST":
        login_form = UserLoginForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Attempt to sign user in
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("PaperTrail_App:dashboard")
            else:
                messages.error(request, "Invalid username and/or password.")
        else:
            messages.error(request, "Invalid email and/or password or submission.")

    return render(
        request,
        "PaperTrail_App/login.html",
        {
            "login_form": login_form,
        },
    )


def user_logout(request):
    logout(request)
    return redirect("PaperTrail_App:user_login")


def dashboard(request):
    return render(request, "PaperTrail_App/dashboard.html")


def upload_docs(request):
    if request.method == "POST":
        doc_form = DocumentForm(request.POST, request.FILES)
        if doc_form.is_valid():
            uploaded_file = request.FILES["document"]

            doc_name = uploaded_file.name
            doc_type = "img"

            new_document = Document(
                doc=uploaded_file,
                doc_name=doc_name,
                owner=request.user,
                doc_type=doc_type,
            )
            new_document.save()
            messages.success(request, "Your file was successfully uploaded.")
        else:
            messages.error(request, "Something isn't quite right ＞︿＜")
    else:
        doc_form = DocumentForm()
    return render(request, "PaperTrail_App/upload.html", {"doc_form": doc_form})
