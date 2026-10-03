from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET

from .forms import RegistrationForm


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("users:profile")

    else:
        form = RegistrationForm()

    return render(
        request,
        "users/register.html",
        {"form": form},
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("users:profile")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("users:profile")

        messages.error(
            request,
            "Invalid username or password.",
        )

    return render(request, "users/login.html")


@login_required
@require_GET
def logout_view(request):
    logout(request)
    return redirect("users:login")


@login_required
def profile(request):
    return render(request, "users/profile.html")