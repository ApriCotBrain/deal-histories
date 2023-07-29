"""Database settings of the 'deals' application."""

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models

from core.enums import Limits, Regex

User = get_user_model()


class Gem(models.Model):
    """Model Gem."""

    name = models.CharField(
        "gem",
        help_text="Gem",
        max_length=Limits.GEM_NAME_MAX_CHAR,
        unique=True,
        validators=(RegexValidator(Regex.GEM_NAME_REGEX),),
    )

    class Meta:
        verbose_name = "gem"
        verbose_name_plural = "gems"
        ordering = ("name",)

    def __str__(self):
        return self.name


class File(models.Model):
    """Model Deal."""

    file = models.FileField(
        "file",
        help_text="Uploaded file",
        upload_to="csv/",
        validators=(FileExtensionValidator(("csv",)),),
    )

    class Meta:
        verbose_name = "file"
        verbose_name_plural = "files"


class Deal(models.Model):
    """Model Deal."""

    file = models.ForeignKey(
        File,
        help_text="Uploaded file",
        related_name="deals",
        on_delete=models.PROTECT,
    )
    user = models.ManyToManyField(
        User,
        verbose_name="user",
        help_text="Customer of the deal",
        related_name="deals",
    )
    item = models.ManyToManyField(
        Gem,
        verbose_name="item",
        help_text="Deal's gems",
        related_name="deals",
    )
    total = models.PositiveIntegerField(
        "total",
        help_text="The total cost of the deal",
    )

    class Meta:
        verbose_name = "deal"
        verbose_name_plural = "deals"

    def __str__(self):
        return self.total
