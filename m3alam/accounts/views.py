from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import ArtisanSignupForm, ClientSignupForm
from .models import User


def signup_client(request):
    form = ClientSignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.role = User.Role.CLIENT
        user.save()
        login(request, user)
        return redirect("home")
    return render(request, "accounts/signup_client.html", {"form": form})


def signup_artisan(request):
    form = ArtisanSignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("home")
    return render(request, "accounts/signup_artisan.html", {"form": form})
