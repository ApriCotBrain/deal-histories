"""Representation of the 'deals' app models in the admin panel."""

from django.contrib import admin

from deals.models import File, Gem, Deal


@admin.register(Gem)
class GemAdmin(admin.ModelAdmin):
    """Representation of the Gem model in the admin panel."""

    list_display = ("name",)


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    """Representation of the Deal model in the admin panel."""

    list_display = ("id", "total", "file")


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    """Representation of the File model in the admin panel."""

    list_display = ("id",)
