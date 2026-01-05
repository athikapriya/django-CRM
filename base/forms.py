from django.forms import ModelForm
from .models import *
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# orderForm starts

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
        exclude = ["customer"]
        widgets = {
            "note": forms.Textarea(
                attrs = {
                    "rows" : 2,
                    "style" : "resize :none",
                    "class" : "mt-2 form-control w-100",
                    "placeholder" : "Max 200 words"
                }
            )
        }

    def clean_note(self):
        note = self.cleaned_data.get("note", "")

        if note:
            word = note.split()
            if len(word) > 200:
                raise ValidationError("Note cannot exceed 200 words.")
        return note
    
# orderForm starts



# userCreation Form starts

class CreateUserForm(UserCreationForm):

    username = forms.CharField(
        label = "Full Name",
        widget= forms.TextInput(attrs={
            "class" : "form-control",
            "placeholder" : "Enter full name"
        })
    )

    email = forms.CharField(
        label = "Email Address",
        widget= forms.EmailInput(attrs={
            "class" : "form-control",
            "placeholder" : "Enter email address"
        })
    )

    password1 = forms.CharField(
        label= "Password",
        widget= forms.PasswordInput(attrs={
            "class" : "form-control password-field",
            "placeholder" : "Create password"
        })
    )

    password2 = forms.CharField(
        label= "Confirm Password",
        widget= forms.PasswordInput(attrs={
            "class" : "form-control password-field",
            "placeholder" : "Re-enter password"
        })
    )


    class Meta:
        model = User
        fields = [ "username", "email", "password1", "password2" ]

# userCreation Form ends