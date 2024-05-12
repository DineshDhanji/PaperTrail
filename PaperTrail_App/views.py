from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from .forms import UserLoginForm, DocumentForm, UserCreationForm
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


def user_signup(request):
    if request.method == "POST":
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            return redirect("PaperTrail_App:dashboard")
    else:
        signup_form = UserCreationForm()
    return render(
        request,
        "PaperTrail_App/signup.html",
        {
            "signup_form": signup_form,
        },
    )


def dashboard(request):
    return render(request, "PaperTrail_App/dashboard.html")


def shared_docs(request):
    return render(request, "PaperTrail_App/shared.html")


def upload_docs(request):
    if request.method == "POST":
        doc_form = DocumentForm(request.POST, request.FILES)
        if doc_form.is_valid():
            uploaded_file = request.FILES["document"]

            doc_name = uploaded_file.name
            doc_type = "img"
            # Determine the file type
            if doc_name.endswith(".pdf"):
                doc_type = "pdf"
            elif doc_name.endswith((".jpg", ".jpeg", ".png")):
                doc_type = "img"
            elif doc_name.endswith(".docx"):
                doc_type = "pdf"
                # Convert DOCX to PDF
                # docx_content = uploaded_file.read()
                # pdf_content = convert_docx_to_pdf(docx_content)
                doc_name = doc_name[:-5] + ".pdf"  # Rename the file with .pdf extension
            else:
                messages.error(
                    request,
                    "Unsupported file format. Please upload a PDF, DOCX, JPG, JPEG, or PNG file.",
                )
                return render(
                    request, "PaperTrail_App/upload.html", {"doc_form": doc_form}
                )
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


def view_doc_img(request, doc_id):
    # Get the requested document by its ID
    document = get_object_or_404(Document, id=doc_id)

    # Check if the current user is the owner of the document
    if request.user == document.owner or request.user in document.shared_with.all():
        # If the user is the owner, render the view template
        return render(request, "PaperTrail_App/view_img.html", {"document": document})
    else:
        # If the user is not the owner, return a 404 error
        return page_not_found_404(request, exception=404)


def view_doc_pdf(request, doc_id):
    # Get the requested document by its ID
    document = get_object_or_404(Document, id=doc_id)

    # Check if the current user is the owner of the document
    if request.user == document.owner or request.user in document.shared_with.all():
        # If the user is the owner, render the view template
        return render(request, "PaperTrail_App/view_pdf.html", {"document": document})
    else:
        # If the user is not the owner, return a 404 error
        return page_not_found_404(request, exception=404)


def page_not_found_404(request, exception=404):
    return render(
        request,
        "PaperTrail_App/404.html",
        status=404,
    )
