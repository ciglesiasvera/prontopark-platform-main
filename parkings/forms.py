from django import forms
from .models import Parking, Lot
from users.models import User


class ParkingForm(forms.ModelForm):
    class Meta:
        model = Parking
        fields = ["number", "visit_parking", "owner", "lot"]
        widgets = {
            "number": forms.TextInput(attrs={"class": "form-control"}),
            #'hourly_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            "visit_parking": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "owner": forms.Select(attrs={"class": "form-select"}),
            "lot": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "number": "Número de estacionamiento",
            "visit_parking": "¿Es estacionamiento de visita?",
            "owner": "Propietario",
            "lot": "Lote",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["owner"].queryset = User.objects.filter(
            role__in=["admin", "supervisor", "resident", "parking_owner"]
        )
        self.fields["lot"].queryset = Lot.objects.all()


class LotForm(forms.ModelForm):
    class Meta:
        model = Lot
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "name": "Nombre de lote",
        }
