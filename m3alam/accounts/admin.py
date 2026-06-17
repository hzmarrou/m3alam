from django.contrib import admin

from .models import ArtisanProfile, User

admin.site.register(User)
admin.site.register(ArtisanProfile)
