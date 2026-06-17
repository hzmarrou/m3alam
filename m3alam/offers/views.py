from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from jobs.models import JobRequest

from .forms import JobOfferForm
from .models import JobOffer


@login_required
def create_offer(request, job_id):
    if request.user.role != "artisan":
        return HttpResponseForbidden("Accès réservé aux artisans.")
    job = get_object_or_404(JobRequest, id=job_id, status=JobRequest.Status.OPEN)
    form = JobOfferForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        offer = form.save(commit=False)
        offer.job = job
        offer.artisan = request.user
        offer.save()
        return redirect("job_detail", job_id=job.id)
    return render(request, "offers/offer_form.html", {"form": form, "job": job})


@login_required
def accept_offer(request, offer_id):
    offer = get_object_or_404(JobOffer.objects.select_related("job"), id=offer_id)
    if request.user != offer.job.client:
        return HttpResponseForbidden("Accès interdit.")
    JobOffer.objects.filter(job=offer.job, status=JobOffer.Status.PENDING).exclude(id=offer.id).update(
        status=JobOffer.Status.REJECTED
    )
    offer.status = JobOffer.Status.ACCEPTED
    offer.save(update_fields=["status"])
    offer.job.status = JobRequest.Status.ASSIGNED
    offer.job.save(update_fields=["status"])
    return redirect("job_detail", job_id=offer.job_id)


@login_required
def client_contact(request, offer_id):
    offer = get_object_or_404(JobOffer.objects.select_related("job__client"), id=offer_id, artisan=request.user)
    if offer.status != JobOffer.Status.ACCEPTED:
        return HttpResponseForbidden("Coordonnées disponibles après acceptation.")
    return render(request, "offers/client_contact.html", {"offer": offer})
