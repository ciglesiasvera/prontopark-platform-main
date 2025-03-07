from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class ResidentRegistrationForm(UserCreationForm):
    phone = forms.CharField(
        label="Número de teléfono",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese su número de teléfono.",
        },
    )
    rut = forms.CharField(
        label="RUT",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese su RUT.",
        },
    )
    rut_dv = forms.CharField(
        label="Dígito verificador",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese el dígito verificador del RUT.",
        },
    )
    first_name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese su nombre.",
        },
    )
    last_name = forms.CharField(
        label="Apellido",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese su apellido.",
        },
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "rut",
            "rut_dv",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override field-specific error messages for inherited fields from UserCreationForm
        self.fields["email"].widget.attrs.update({"class": "form-control"})
        self.fields["email"].label = "Correo electrónico"
        self.fields["email"].error_messages.update(
            {
                "required": "Por favor, ingrese su correo electrónico.",
                "invalid": "Por favor, ingrese un correo electrónico válido.",
                "unique": "Este correo electrónico ya está registrado.",
            }
        )
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].label = "Contraseña"
        self.fields["password1"].error_messages.update(
            {
                "required": "Por favor, ingrese una contraseña.",
            }
        )
        self.fields["password2"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].label = "Confirmar contraseña"
        self.fields["password2"].error_messages.update(
            {
                "required": "Por favor, confirme su contraseña.",
                "password_mismatch": "Las contraseñas no coinciden.",
            }
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.phone = self.cleaned_data["phone"]
        user.rut = self.cleaned_data["rut"]
        user.rut_dv = self.cleaned_data["rut_dv"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.role = "resident"  # Establece el rol como residente
        if commit:
            user.save()
        return user


class ParkingOwnerRegistrationForm(UserCreationForm):
    phone = forms.CharField(
        label="Número de teléfono",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese su número de teléfono.",
        },
    )
    rut = forms.CharField(
        label="RUT",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese su RUT.",
        },
    )
    rut_dv = forms.CharField(
        label="Dígito verificador",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese el dígito verificador del RUT.",
        },
    )
    first_name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese su nombre.",
        },
    )
    last_name = forms.CharField(
        label="Apellido",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese su apellido.",
        },
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "rut",
            "rut_dv",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override field-specific error messages for inherited fields from UserCreationForm
        self.fields["email"].widget.attrs.update({"class": "form-control"})
        self.fields["email"].label = "Correo electrónico"
        self.fields["email"].error_messages.update(
            {
                "required": "Por favor, ingrese su correo electrónico.",
                "invalid": "Por favor, ingrese un correo electrónico válido.",
                "unique": "Este correo electrónico ya está registrado.",
            }
        )
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].label = "Contraseña"
        self.fields["password1"].error_messages.update(
            {
                "required": "Por favor, ingrese una contraseña.",
            }
        )
        self.fields["password2"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].label = "Confirmar contraseña"
        self.fields["password2"].error_messages.update(
            {
                "required": "Por favor, confirme su contraseña.",
                "password_mismatch": "Las contraseñas no coinciden.",
            }
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.phone = self.cleaned_data["phone"]
        user.rut = self.cleaned_data["rut"]
        user.rut_dv = self.cleaned_data["rut_dv"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.role = "parking_owner"  # Establece el rol como parking_owner
        if commit:
            user.save()
        return user


class ConciergeRegistrationForm(UserCreationForm):
    phone = forms.CharField(
        label="Número de teléfono",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese su número de teléfono.",
        },
    )
    rut = forms.CharField(
        label="RUT",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese su RUT.",
        },
    )
    rut_dv = forms.CharField(
        label="Dígito verificador",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese el dígito verificador del RUT.",
        },
    )
    first_name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese su nombre.",
        },
    )
    last_name = forms.CharField(
        label="Apellido",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese su apellido.",
        },
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "rut",
            "rut_dv",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override field-specific error messages for inherited fields from UserCreationForm
        self.fields["email"].widget.attrs.update({"class": "form-control"})
        self.fields["email"].label = "Correo electrónico"
        self.fields["email"].error_messages.update(
            {
                "required": "Por favor, ingrese su correo electrónico.",
                "invalid": "Por favor, ingrese un correo electrónico válido.",
                "unique": "Este correo electrónico ya está registrado.",
            }
        )
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].label = "Contraseña"
        self.fields["password1"].error_messages.update(
            {
                "required": "Por favor, ingrese una contraseña.",
            }
        )
        self.fields["password2"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].label = "Confirmar contraseña"
        self.fields["password2"].error_messages.update(
            {
                "required": "Por favor, confirme su contraseña.",
                "password_mismatch": "Las contraseñas no coinciden.",
            }
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.phone = self.cleaned_data["phone"]
        user.rut = self.cleaned_data["rut"]
        user.rut_dv = self.cleaned_data["rut_dv"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.role = "concierge"  # Establece el rol como concierge
        if commit:
            user.save()
        return user


class AdminRegistrationForm(UserCreationForm):
    phone = forms.CharField(
        label="Número de teléfono",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese su número de teléfono.",
        },
    )
    rut = forms.CharField(
        label="RUT",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese su RUT.",
        },
    )
    rut_dv = forms.CharField(
        label="Dígito verificador",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese el dígito verificador del RUT.",
        },
    )
    first_name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese su nombre.",
        },
    )
    last_name = forms.CharField(
        label="Apellido",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Por favor, ingrese su apellido.",
        },
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "rut",
            "rut_dv",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override field-specific error messages for inherited fields from UserCreationForm
        self.fields["email"].widget.attrs.update({"class": "form-control"})
        self.fields["email"].label = "Correo electrónico"
        self.fields["email"].error_messages.update(
            {
                "required": "Por favor, ingrese su correo electrónico.",
                "invalid": "Por favor, ingrese un correo electrónico válido.",
                "unique": "Este correo electrónico ya está registrado.",
            }
        )
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].label = "Contraseña"
        self.fields["password1"].error_messages.update(
            {
                "required": "Por favor, ingrese una contraseña.",
            }
        )
        self.fields["password2"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].label = "Confirmar contraseña"
        self.fields["password2"].error_messages.update(
            {
                "required": "Por favor, confirme su contraseña.",
                "password_mismatch": "Las contraseñas no coinciden.",
            }
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.phone = self.cleaned_data["phone"]
        user.rut = self.cleaned_data["rut"]
        user.rut_dv = self.cleaned_data["rut_dv"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.role = "admin"  # Establece el rol como admin
        user.is_staff = True  # Admin debe tener is_staff=True
        if commit:
            user.save()
        return user
