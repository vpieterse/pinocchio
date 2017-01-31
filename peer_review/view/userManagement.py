from django.shortcuts import render
from peer_review.forms import ResetForm


def forgot_password(request):
    reset_form = ResetForm()
    context = {'resetForm': reset_form}
    return render(request, 'peer_review/forgotPassword.html', context)

