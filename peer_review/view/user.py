from django.http import HttpResponseForbidden
from django.shortcuts import render


def user_error(request):
    # Renders error page with a 403 status code for forbidden users
    return HttpResponseForbidden(render(request, 'peer_review/userError.html'))