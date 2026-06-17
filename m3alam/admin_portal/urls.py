from django.urls import path

from .views import dashboard, hide_job, suspend_user

urlpatterns = [
    path("", dashboard, name="admin_dashboard"),
    path("masquer-travail/<int:job_id>/", hide_job, name="admin_hide_job"),
    path("suspendre-utilisateur/<int:user_id>/", suspend_user, name="admin_suspend_user"),
]
