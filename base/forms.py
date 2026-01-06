from django.forms import ModelForm
from .models import *
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .validators import PasswordComplexityValidator

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
        error_messages= {
            "required": "This field is required.",
            "unique": "This username is already taken.",
            "max_length": "Username is too long.",
        },
        widget= forms.TextInput(attrs={
            "class" : "form-control",
            "placeholder" : "Enter full name"
        })
    )

    email = forms.EmailField(
        label = "Email Address",
        error_messages= {
            "required" : "Email is required",
            "invalid" : "Enter a valid email address."
        },
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
        }),
        required=True
    )

    password2 = forms.CharField(
        label= "Confirm Password",
        widget= forms.PasswordInput(attrs={
            "class" : "form-control password-field",
            "placeholder" : "Re-enter password"
        }),
        required=True
    )


    class Meta:
        model = User
        fields = [ "username", "email", "password1", "password2" ]

    def clean(self):
        
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        validator = PasswordComplexityValidator()

        if not password1 or not password2:
            self.add_error(
                "password2",
                "Password must be at least 8 characters and include a capital letter, a number, a symbol, and lowercase letters."
            )
            return cleaned_data

        
        try:
            validator.validate(password1)
        except ValidationError:
            
            self.add_error(
                "password2",
                "Password must be at least 8 characters and include a capital letter, a number, a symbol, and lowercase letters."
            )
            return cleaned_data

        if password1 != password2:
            self.add_error("password2", "The two password fields didn’t match.")

        return cleaned_data

    def save(self, commit=True):
        """
        Save user with proper password hashing
        """
        user = User(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"]
        )
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

# userCreation Form ends