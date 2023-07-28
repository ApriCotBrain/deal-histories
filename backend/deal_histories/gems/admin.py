"""Representation of the 'gems' app models in the admin panel."""

from django.contrib import admin

from gems.models import Gem


@admin.register(Gem)
class GemAdmin(admin.ModelAdmin):
    """Representation of the User model in the admin panel."""

    list_display = ("name",)
