from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import JobRequestForm
from .models import JobRequest


@login_required
def create_job(request):
    if request.user.role != "client":
        return HttpResponseForbidden("Accès réservé aux clients.")
    form = JobRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        job = form.save(commit=False)
        job.client = request.user
        job.save()
        return redirect("job_detail", job_id=job.id)
    return render(request, "jobs/job_form.html", {"form": form})


def list_jobs(request):
    jobs = JobRequest.objects.filter(status=JobRequest.Status.OPEN)
    return render(request, "jobs/job_list.html", {"jobs": jobs})


def job_detail(request, job_id):
    job = get_object_or_404(JobRequest, id=job_id)
    return render(request, "jobs/job_detail.html", {"job": job})
