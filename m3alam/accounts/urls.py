from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .forms import FrenchAuthenticationForm
from .views import signup_artisan, signup_client

urlpatterns = [
    path("inscription-client/", signup_client, name="signup_client"),
    path("inscription-artisan/", signup_artisan, name="signup_artisan"),
    path(
        "connexion/",
        LoginView.as_view(template_name="accounts/login.html", authentication_form=FrenchAuthenticationForm),
        name="login",
    ),
    path("deconnexion/", LogoutView.as_view(), name="logout"),
]
