from django import forms

from .models import JobRequest


class JobRequestForm(forms.ModelForm):
    class Meta:
        model = JobRequest
        fields = ("category", "title", "description", "city", "budget_min", "budget_max")
        labels = {
            "category": "Catégorie",
            "title": "Titre",
            "description": "Description",
            "city": "Ville",
            "budget_min": "Budget min (MAD)",
            "budget_max": "Budget max (MAD)",
        }
