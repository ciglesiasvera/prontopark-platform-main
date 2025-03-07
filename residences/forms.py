# residences/forms.py
from django import forms
from .models import BlockName, Residence
from users.models import User


class BlockNameForm(forms.ModelForm):
    class Meta:
        model = BlockName
        fields = ["name"]
        labels = {"name": "Block Name"}
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}
        labels = {"name": "Nombre del Bloque"}


class ResidenceForm(forms.ModelForm):
    class Meta:
        model = Residence
        fields = ["number", "block_name", "owner"]
        widgets = {
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "block_name": forms.Select(attrs={"class": "form-select"}),
            "owner": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "number": "Número de Residencia",
            "block_name": "Nombre del Bloque",
            "owner": "Propietario",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["owner"].queryset = User.objects.filter(
            role__in=["admin", "supervisor", "resident", "parking_owner"]
        )
