from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.registerPage, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),

    path('unauthorized/', views.unauthorized, name='unauthorized'),

    path("", views.homepage, name="homepage"),
    
    path('products/', views.products, name="products"),
    path('customer/<str:pk>', views.customer, name="customer"),
    path("create_order/<str:pk>/", views.CreateOrder, name="create_order"),
    path("update_order/<str:pk>/", views.UpdateOrder, name="update_order"),
    path("delete_order/<str:pk>/", views.DeleteOrder, name="delete_order"),

    path("<str:username>/account_settings/", views.accountSettings, name="settings"),
    path("<str:username>/", views.userProfile, name="user_profile"),
]
