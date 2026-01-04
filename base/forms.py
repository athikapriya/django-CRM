from django.forms import ModelForm
from .models import *
from django import forms
from django.core.exceptions import ValidationError

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