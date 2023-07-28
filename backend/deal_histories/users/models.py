"""Database settings of the 'users' application."""

from django.contrib.auth.models import AbstractUser
from django.db import models

from core.enums import Limits


class User(AbstractUser):
    """Modified model User."""

    first_name = None
    last_name = None
    spent_money = models.PositiveIntegerField(
        "spent money",
        help_text="The spent money for the entire period",
        default=Limits.USER_SPENT_MONEY_VALUE,
    )

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ("username",)

    def __str__(self):
        return self.username
