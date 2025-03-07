from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Reservation, ReservationStatus
from parkings.models import Parking


class ReservationForm(forms.ModelForm):

    parking = forms.ModelChoiceField(
        queryset=Parking.objects.all(),
        label=_("Selecciona un estacionamiento"),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
    )
    start_datetime = forms.DateTimeField(
        label=_("Inicio"),
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        ),
        required=True,
    )
    end_datetime = forms.DateTimeField(
        label=_("Término"),
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        ),
        required=True,
    )
    comments = forms.CharField(
        label=_("Comentarios"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        model = Reservation
        fields = ["parking", "start_datetime", "end_datetime", "comments"]

    def clean(self):
        """
        Validate reservation dates and parking availability
        """
        cleaned_data = super().clean()
        start_datetime = cleaned_data.get("start_datetime")
        end_datetime = cleaned_data.get("end_datetime")
        parking = cleaned_data.get("parking")

        # Validate datetime range
        if start_datetime and end_datetime:
            if start_datetime >= end_datetime:
                raise forms.ValidationError(
                    _("El tiempo de término debe ser mayor al tiempo de inicio.")
                )

        # Check for overlapping reservations
        if parking and start_datetime and end_datetime:
            overlapping_reservations = Reservation.objects.filter(
                parking=parking,
                status__in=[ReservationStatus.PENDING, ReservationStatus.CONFIRMED],
                start_datetime__lt=end_datetime,
                end_datetime__gt=start_datetime,
            )
            if overlapping_reservations.exists():
                raise forms.ValidationError(
                    _(
                        "Este estacionamiento ya fue reservado para la hora seleccionada."
                    )
                )

        return cleaned_data
