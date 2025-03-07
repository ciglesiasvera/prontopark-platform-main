from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Alert
from parkings.models import Parking

class AlertForm(forms.ModelForm):
    """
    Form for creating and updating alerts
    """
    parking = forms.ModelChoiceField(
        queryset=Parking.objects.all(),
        label=_('Select Parking'),
        required=True
    )
    description = forms.CharField(
        label=_('Description'),
        widget=forms.Textarea(attrs={'rows': 3}),
        required=True
    )

    class Meta:
        model = Alert
        fields = [
            'parking',
            'description'
        ]
