import django_filters
from .models import Order
from django import forms
from django_filters import CharFilter, DateFilter, ChoiceFilter, ModelChoiceFilter

class OrderFilter(django_filters.FilterSet):

    product = ModelChoiceFilter(
        queryset=Order._meta.get_field("product").related_model.objects.all(),
        empty_label="All Products",
        widget = forms.Select(attrs={
        "class" : "form-select",
        "data-auto-submit": "true"
        })
    )

    status = ChoiceFilter(
        choices = Order.STATUS,
        empty_label = "Order Status",
        widget = forms.Select(attrs={
        "class" : "form-select",
        "data-auto-submit": "true"
        })
    )

    start_date = DateFilter(
        field_name="date_created",
        lookup_expr="gte",
        label = "From date",
        widget = forms.DateInput(attrs={
            "type" : "date",
            "class" : "form-control form-control-sm",
            "data-auto-submit": "true"
        })
    )

    end_date = DateFilter(
        field_name="date_created",
        lookup_expr='lte',
        label = "To date",
        widget = forms.DateInput(attrs={
            "type" : "date",
            "class" : "form-control form-control-sm",
            "data-auto-submit": "true"
        }) 
    )

    note = CharFilter(
        field_name="note",
        lookup_expr="icontains",
        label = "Keyword",
        widget = forms.TextInput(attrs={
            "placeholder" : "Search by Keyword...",
            "class" : "form-control",
            "data-auto-submit": "true"
        })
    )
    

    class Meta :
        model = Order
        fields = []

       