from django.contrib import admin
from .models import Customer, Tag, Product

admin.site.register(Customer)
admin.site.register(Tag)
admin.site.register(Product)