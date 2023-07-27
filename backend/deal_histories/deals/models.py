"""Database settings of the 'Deals' application."""

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

    def __str__(self):
        return self.name


class Deal(models.Model):
    """Model Deal."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="user",
        help_text="Customer of the deal",
        on_delete=models.PROTECT,
        related_name="deals",
    )
    item = models.ForeignKey(
        Gem,
        verbose_name="item",
        help_text="Deal stone",
        on_delete=models.PROTECT,
        related_name="deals",
    )
    total = models.PositiveIntegerField(
        "total",
        help_text="The total cost of the deal",
        default=Limits.DEAL_TOTAL_DEFAULT_VALUE,
    )
    quantity = models.PositiveSmallIntegerField(
        "quantity",
        help_text="The number of gems in the deal",
        default=Limits.DEAL_QUANTITY_DEFAULT_VALUE,
    )
    date = models.DateTimeField(
        "date",
        help_text="deal time",
    )

    class Meta:
        verbose_name = "deal"
        verbose_name_plural = "deals"

    def __str__(self):
        return f"Purchase of a {self.item} by a {self.user}"
