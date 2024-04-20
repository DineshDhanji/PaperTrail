from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import UserLoginForm


def user_login(request):
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
                return render(
                    request,
                    "PaperTrail_App/login.html",
                    {
                        "login_form": login_form,
                    },
                )
        else:
            messages.error(request, "Invalid email and/or password or submission.")
            return render(
                request,
                "PaperTrail_App/login.html",
                {
                    "login_form": login_form,
                },
            )
    else:
        if request.user.is_authenticated:
            return redirect("PaperTrail_App:dashboard")
        else:
            return render(
                request,
                "PaperTrail_App/login.html",
                {
                    "login_form": UserLoginForm(),
                },
            )


def user_logout(request):
    logout(request)
    return redirect("PaperTrail_App:user_login")


def dashboard(request):
    return render(request, "PaperTrail_App/dashboard.html")
