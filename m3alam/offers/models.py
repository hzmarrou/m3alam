from django.conf import settings
from django.db import models

from jobs.models import JobRequest


class JobOffer(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        ACCEPTED = "accepted", "Acceptée"
        REJECTED = "rejected", "Refusée"
        WITHDRAWN = "withdrawn", "Retirée"

    job = models.ForeignKey(JobRequest, on_delete=models.CASCADE, related_name="offers")
    artisan = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="offers")
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("job", "artisan"), name="unique_offer_per_artisan_job"),
        ]
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"Offre {self.id} - {self.artisan.email}"
