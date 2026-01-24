from django.forms import ModelForm, ClearableFileInput
from .models import *
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .validators import PasswordComplexityValidator


# customerForm starts 

class CustomClearableFileInput(ClearableFileInput):
    template_name = 'widgets/custom_clearable_file_input.html'


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'profile_pic']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Email Address'}),
            'profile_pic': CustomClearableFileInput(attrs={'style': 'display:none;'}),  # use our custom widget
        }

# customerForm ends

# orderForm starts

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
        exclude = ["customer"]

        widgets = {
            "product": forms.Select(attrs={
                "class": "form-select",
            }),
            "status": forms.Select(attrs={
                "class": "form-select",
            }),
            "note": forms.Textarea(attrs={
                "rows": 2,
                "style": "resize:none",
                "class": "form-control",
                "placeholder": "Max 200 words"
            }),
        }

    def clean_note(self):
        note = self.cleaned_data.get("note", "")
        if note and len(note.split()) > 200:
            raise ValidationError("Note cannot exceed 200 words.")
        return note

    
# orderForm ends



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


# Request OTP and verify OTP forms starts

class RequestOTPForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )


class VerifyOTPForm(forms.Form):
    otp = forms.CharField(max_length=6, label="Enter OTP")


class SetNewPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control password-field', 'placeholder': 'New Password'}),
        label="New Password",
        required=True
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control password-field', 'placeholder': 'Confirm Password'}),
        label="Confirm Password",
        required=True
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        validator = PasswordComplexityValidator()

        if not password1:
            raise ValidationError(
                "Password must be at least 8 characters and include a capital letter, a number, a symbol, and lowercase letters."
            )

        try:
            validator.validate(password1)
        except ValidationError:
            raise ValidationError(
                "Password must be at least 8 characters and include a capital letter, a number, a symbol, and lowercase letters."
            )

        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields didn’t match.")

        return password2


# Request OTP and verify OTP forms ends