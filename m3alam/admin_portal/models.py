from django.conf import settings
from django.db import models


class AdminAuditLog(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="admin_actions")
    action_type = models.CharField(max_length=50)
    target_type = models.CharField(max_length=50)
    target_id = models.IntegerField()
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.action_type} {self.target_type}#{self.target_id}"
