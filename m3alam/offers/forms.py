from django import forms

from .models import JobOffer


class JobOfferForm(forms.ModelForm):
    class Meta:
        model = JobOffer
        fields = ("proposed_price", "message")
        labels = {
            "proposed_price": "Prix proposé (MAD)",
            "message": "Message",
        }
