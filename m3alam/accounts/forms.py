from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import ArtisanProfile, User


class ClientSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "phone")


class ArtisanSignupForm(UserCreationForm):
    full_name = forms.CharField(label="Nom complet")
    city = forms.CharField(label="Ville")
    skills = forms.CharField(label="Compétences")
    bio = forms.CharField(label="Bio", widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ("email", "phone")

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        user.role = User.Role.ARTISAN
        if commit:
            user.save()
            ArtisanProfile.objects.create(
                user=user,
                full_name=self.cleaned_data["full_name"],
                city=self.cleaned_data["city"],
                skills=self.cleaned_data["skills"],
                bio=self.cleaned_data["bio"],
            )
        return user


class FrenchAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
