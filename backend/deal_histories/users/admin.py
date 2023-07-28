"""Representation of the 'users' app models in the admin panel."""

from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Representation of the User model in the admin panel."""

    list_display = (
        "username",
        "spent_money",
    )
