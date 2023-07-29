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

    class Meta:
        verbose_name = "gem"
        verbose_name_plural = "gems"
        ordering = ("name",)

    def __str__(self):
        return self.name


class File(models.Model):
    file = models.FileField(upload_to="csv/")


class Deal(models.Model):
    """Model Deal."""

    file = models.ForeignKey(
        File, related_name="deals", on_delete=models.PROTECT
    )

    user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="user",
        help_text="Customer of the deal",
        related_name="deals",
    )
    item = models.ManyToManyField(
        Gem,
        verbose_name="item",
        help_text="Deal stone",
        related_name="deals",
    )
    total = models.PositiveIntegerField(
        "total",
        help_text="The total cost of the deal",
        default=Limits.DEAL_TOTAL_DEFAULT_VALUE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "deal"
        verbose_name_plural = "deals"

    def __str__(self):
        return f"Purchase of a {self.item} by a {self.user}"
