from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Report

class ReportForm(forms.ModelForm):
    """
    Form for creating and updating reports
    """
    REPORT_TYPE_CHOICES = (
        ('reservation', _('Reservation')),
        ('alert', _('Alert')),
    )

    report_type = forms.ChoiceField(
        choices=REPORT_TYPE_CHOICES,
        label=_('Report Type'),
        required=True
    )
    start_date = forms.DateField(
        label=_('Start Date'),
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    end_date = forms.DateField(
        label=_('End Date'),
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    class Meta:
        model = Report
        fields = [
            'report_type',
            'start_date',
            'end_date',
        ]
