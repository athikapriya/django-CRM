from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        
        if request.path.startswith("/reset") or request.path.startswith("/reset_password"):
            return view_func(request, *args, **kwargs)

        if request.user.is_authenticated:
            return redirect("homepage")
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func



def allowed_users(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            # Skip all password reset URLs
            if request.resolver_match.url_name in [
                "password_reset",
                "password_reset_done",
                "password_reset_confirm",
                "password_reset_complete"
            ]:
                return view_func(request, *args, **kwargs)

            if not request.user.is_authenticated:
                return redirect("login")

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            user_groups = list(request.user.groups.values_list("name", flat=True))
            if any(role in user_groups for role in allowed_roles):
                return view_func(request, *args, **kwargs)

            messages.error(request, "You do not have permission to access this page.")
            return redirect("unauthorized")

        return wrapper_func
    return decorator



def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):

        # Skip password reset views
        if request.resolver_match.url_name in [
            "password_reset",
            "password_reset_done",
            "password_reset_confirm",
            "password_reset_complete"
        ]:
            return view_func(request, *args, **kwargs)

        if not request.user.is_authenticated:
            return redirect("login")

        if request.user.is_superuser or request.user.groups.filter(name="admin").exists():
            return view_func(request, *args, **kwargs)

        return redirect("unauthorized")

    return wrapper_func
