from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import EmailField, CharField, ModelForm, Form
from django.utils.translation import gettext_lazy as _
from .models import ShippingInfo, Product


class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"placeholder": field.label})


class CustomUserCreationForm(UserCreationForm):
    email = EmailField(label=_("Email"), required=True)
    first_name = CharField(label=_("First name"), max_length=150, required=True)
    last_name = CharField(label=_("Last name"), max_length=150, required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"placeholder": field.label})

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("An user with this email already exists!")
        return email


class ShippingInfoForm(ModelForm):
    class Meta:
        model = ShippingInfo
        fields = ["city", "address", "zipcode"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"placeholder": field.label})


class ContactInfoForm(Form):
    email = EmailField(label=_("Email"), required=True)
    first_name = CharField(label=_("First name"), max_length=150, required=True)
    last_name = CharField(label=_("Last name"), max_length=150, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"placeholder": field.label})


class ProductCreationForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'placeholder': field.label})