from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('products/', views.products, name="products"),
    path('customer/<str:pk>', views.customer, name="customer"),
    path("create_order/<str:pk>/", views.CreateOrder, name="create_order"),
    path("update_order/<str:pk>/", views.UpdateOrder, name="update_order"),
    path("delete_order/<str:pk>/", views.DeleteOrder, name="delete_order"),
]
