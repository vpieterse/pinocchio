from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

from functools import wraps

from django.http.response import HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import redirect


def admin_required_test(user):
    if user.is_active and user.is_authenticated:
        if user.status == 'A' or user.is_superuser:
            return True

    return False


def admin_required(function=None, redirect_field_name=None, login_url='/login/'):
    """
    Decorator for views that checks that the user is logged in
    and has the "admin" permission set. Users with an 'A' status
    field are considered admin.
    """

    def _decorated(view_func):
        def _view(request, *args, **kwargs):
            if admin_required_test(request.user):
                return view_func(request, *args, **kwargs)
            else:
                #return view_func(request, *args, **kwargs)
                return redirect(login_url)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _decorated
    else:
        return _decorated(function)