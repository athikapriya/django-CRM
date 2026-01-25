from django.urls import path
from django.contrib.auth import views as auth_views

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

    path("reset_password/", auth_views.PasswordResetView.as_view(template_name="base/password_reset.html"), name="password_reset"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(template_name="base/reset_password_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="base/password_reset_confirm.html"), name='password_reset_confirm'),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="base/password_reset_complete.html"), name="password_reset_complete"),

    path('password_reset_otp/', views.request_password_otp, name='password_reset_otp'),
    path('password_reset_verify/', views.verify_otp, name='verify_otp'),
    path('password_reset_now/', views.password_reset_now, name='password_reset_now'),

    path("<str:username>/account_settings/", views.accountSettings, name="settings"),
    path("<str:username>/", views.userProfile, name="user_profile"),
]
