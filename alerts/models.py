from django.db import models
from django.utils.translation import gettext_lazy as _
from parkings.models import Parking
from users.models import User

class AlertStatus(models.TextChoices):
    """
    Enum for alert status
    """
    PENDING = 'PENDING', _('Pending')
    RESOLVED = 'RESOLVED', _('Resolved')
    DISMISSED = 'DISMISSED', _('Dismissed')

class Alert(models.Model):
    """
    Model to manage alerts
    """
    parking = models.ForeignKey(
        Parking,
        on_delete=models.CASCADE,
        verbose_name=_('Parking')
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User')
    )
    description = models.TextField(
        verbose_name=_('Description')
    )
    status = models.CharField(
        max_length=20,
        choices=AlertStatus.choices,
        default=AlertStatus.PENDING,
        verbose_name=_('Alert Status')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )

    def __str__(self):
        return f"Alert for {self.parking.number} by {self.user.email}"

    class Meta:
        verbose_name = _('Alert')
        verbose_name_plural = _('Alerts')
        ordering = ['-created_at']
