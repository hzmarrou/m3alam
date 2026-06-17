from django.urls import path

from .views import create_job, job_detail, list_jobs

urlpatterns = [
    path("", list_jobs, name="job_list"),
    path("nouveau/", create_job, name="job_create"),
    path("<int:job_id>/", job_detail, name="job_detail"),
]
