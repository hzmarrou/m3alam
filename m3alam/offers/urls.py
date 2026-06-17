from django.urls import path

from .views import accept_offer, client_contact, create_offer

urlpatterns = [
    path("creer/<int:job_id>/", create_offer, name="offer_create"),
    path("accepter/<int:offer_id>/", accept_offer, name="offer_accept"),
    path("contact-client/<int:offer_id>/", client_contact, name="client_contact"),
]
