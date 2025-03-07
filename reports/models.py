from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User

class Report(models.Model):
    """
    Model to manage reports
    """
    REPORT_TYPE_CHOICES = (
        ('reservation', _('Reservation')),
        ('alert', _('Alert')),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User')
    )
    report_type = models.CharField(
        max_length=20,
        choices=REPORT_TYPE_CHOICES,
        verbose_name=_('Report Type')
    )
    start_date = models.DateField(
        verbose_name=_('Start Date')
    )
    end_date = models.DateField(
        verbose_name=_('End Date')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )

    def __str__(self):
        return f"Report for {self.user.username} ({self.report_type})"

    class Meta:
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')
        ordering = ['-created_at']
