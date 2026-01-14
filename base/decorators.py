from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def unauthenticated_user(viwe_func):
    def wrapper_func(request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect("homepage")
        else:
            return viwe_func(request, *args, **kwargs)
    return wrapper_func



def allowed_users(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorators(view_func):

        @login_required(login_url="login")
        def wrapper_func(request, *args, **kwargs):

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            user_groups = request.user.groups.values_list("name", flat=True)

            if any(role in user_groups for role in allowed_roles):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You do not have permission to access this page.")
                return redirect("unauthorized")
            
        return wrapper_func
    return decorators


def admin_only(view_func):
    @login_required(login_url="login")
    def wrapper_func(request, *args, **kwargs):

        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        if request.user.groups.filter(name="admin").exists():
            return view_func(request, *args, **kwargs)

        return redirect("unauthorized")

    return wrapper_func