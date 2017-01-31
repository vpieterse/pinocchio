from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def admin_required_test(user):
    if user.is_active and user.is_authenticated:
        if user.status == 'A' or user.is_superuser:
            return True

    return False

def admin_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                   login_url='/login/'):
    """
    Decorator for views that checks that the user is logged in
    and has the "admin" permission set. Users with an 'A' status
    field are considered admin.
    """
    actual_decorator = user_passes_test(
        admin_required_test,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
