"""Database settings of the 'Deals' application."""

from django.contrib.auth.models import AbstractUser
from django.db import models

from core.enums import Limits
from deals.models import Gem


class User(AbstractUser):
    """Modified model User."""

    first_name = None
    last_name = None
    spent_money = models.PositiveIntegerField(
        "spent money",
        help_text="The spent money for the entire period",
        default=Limits.USER_SPENT_MONEY_VALUE,
    )
    gems = models.ManyToManyField(
        Gem,
        verbose_name="gems",
        help_text="User's gems",
        related_name="users",
    )

    class Meta:
        ordering = ("username",)
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.username
