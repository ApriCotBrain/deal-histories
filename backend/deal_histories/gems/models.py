"""Database settings of the 'deals' application."""

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from core.enums import Limits, Regex


class Gem(models.Model):
    """Model Gem."""

    name = models.CharField(
        "gem",
        help_text="Gem",
        max_length=Limits.GEM_NAME_MAX_CHAR,
        unique=True,
        validators=(RegexValidator(Regex.GEM_NAME),),
    )
    user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="user",
        help_text="The owner of the gem",
        related_name="gems",
    )

    class Meta:
        verbose_name = "gem"
        verbose_name_plural = "gems"
        ordering = ("name",)

    def __str__(self):
        return self.name
