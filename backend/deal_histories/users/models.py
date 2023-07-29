"""Database settings of the 'users' application."""

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Modified model User."""

    first_name = None
    last_name = None

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ("username",)

    def __str__(self):
        return self.username
