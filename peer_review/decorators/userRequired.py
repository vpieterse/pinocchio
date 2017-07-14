from django.shortcuts import redirect

def user_required(function=None, login_url='/login/'):
    """
    Wrapper of Django's login_required to add custom behaviour and redirects.
    """

    def _decorated(view_func):
        def _view(request, *args, **kwargs):
            if request.user.is_authenticated():
                return view_func(request, *args, **kwargs)
            else:
                return redirect(login_url)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _decorated
    else:
        return _decorated(function)