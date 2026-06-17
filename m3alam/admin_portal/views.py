from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from jobs.models import JobRequest

from .models import AdminAuditLog


def _must_be_admin(user):
    return user.is_authenticated and user.role == User.Role.ADMIN


@login_required
def dashboard(request):
    if not _must_be_admin(request.user):
        return HttpResponseForbidden("Accès administrateur uniquement.")
    context = {
        "users_count": User.objects.count(),
        "artisans_count": User.objects.filter(role=User.Role.ARTISAN).count(),
        "jobs_open": JobRequest.objects.filter(status=JobRequest.Status.OPEN).count(),
        "logs": AdminAuditLog.objects.all()[:10],
    }
    return render(request, "admin_portal/dashboard.html", context)


@login_required
def hide_job(request, job_id):
    if not _must_be_admin(request.user):
        return HttpResponseForbidden("Accès administrateur uniquement.")
    job = get_object_or_404(JobRequest, id=job_id)
    job.status = JobRequest.Status.HIDDEN
    job.save(update_fields=["status"])
    AdminAuditLog.objects.create(
        admin=request.user, action_type="hide", target_type="job", target_id=job.id, reason="Modération"
    )
    return redirect("admin_dashboard")


@login_required
def suspend_user(request, user_id):
    if not _must_be_admin(request.user):
        return HttpResponseForbidden("Accès administrateur uniquement.")
    target = get_object_or_404(User, id=user_id)
    target.is_active = False
    target.save(update_fields=["is_active"])
    AdminAuditLog.objects.create(
        admin=request.user, action_type="suspend", target_type="user", target_id=target.id, reason="Modération"
    )
    return redirect("admin_dashboard")
