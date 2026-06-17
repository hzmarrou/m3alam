from django import forms

from .models import JobRequest
from .service_catalog import SERVICE_CATEGORIES


class JobRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"] = forms.ChoiceField(
            label="Catégorie",
            choices=SERVICE_CATEGORIES,
        )

    class Meta:
        model = JobRequest
        fields = ("category", "title", "description", "city", "budget_min", "budget_max")
        labels = {
            "title": "Titre",
            "description": "Description",
            "city": "Ville",
            "budget_min": "Budget min (MAD)",
            "budget_max": "Budget max (MAD)",
        }
