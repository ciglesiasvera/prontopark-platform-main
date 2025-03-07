from django.db import models
from django.utils.translation import gettext_lazy as _
from parkings.models import Parking
from users.models import User

class ReservationStatus(models.TextChoices):
    """
    Enum for reservation status
    """
    PENDING = 'PENDING', _('Pending')
    CONFIRMED = 'CONFIRMED', _('Confirmed')
    CANCELLED = 'CANCELLED', _('Cancelled')
    COMPLETED = 'COMPLETED', _('Completed')

class Reservation(models.Model):
    """
    Model to manage parking reservations
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
    start_datetime = models.DateTimeField(
        verbose_name=_('Start Date and Time')
    )
    end_datetime = models.DateTimeField(
        verbose_name=_('End Date and Time')
    )
    status = models.CharField(
        max_length=20,
        choices=ReservationStatus.choices,
        default=ReservationStatus.PENDING,
        verbose_name=_('Reservation Status')
    )
    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Additional Comments')
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
        return f"{self.parking.number} ({self.start_datetime})"

    class Meta:
        verbose_name = _('Reservation')
        verbose_name_plural = _('Reservations')
        ordering = ['-created_at']
        unique_together = ['parking', 'start_datetime', 'end_datetime']
