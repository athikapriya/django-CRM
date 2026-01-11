from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(viwe_func):
    def wrapper_func(request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect("homepage")
        else:
            return viwe_func(request, *args, **kwargs)
    return wrapper_func