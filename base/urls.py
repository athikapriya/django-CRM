from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('products/', views.products, name="products"),
    path('customer/', views.customer, name="customer"),
]
