from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from peer_review.email import generate_email
from peer_review.forms import ResetForm, UserForm
from peer_review.generate_otp import generate_otp
from peer_review.models import User, RoundDetail, TeamDetail
from peer_review.decorators.adminRequired import admin_required


def forgot_password(request):
    reset_form = ResetForm()
    context = {'resetForm': reset_form}
    return render(request, 'peer_review/forgotPassword.html', context)


@admin_required
def submit_new_user_form(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            post_title = user_form.cleaned_data['title']
            post_initials = user_form.cleaned_data['initials']
            post_name = user_form.cleaned_data['name']
            post_surname = user_form.cleaned_data['surname']
            post_cell = user_form.cleaned_data['cell']
            post_email = user_form.cleaned_data['email']
            post_user_id = user_form.cleaned_data['userId']

            #user = User(title=post_title, initials=post_initials, name=post_name, surname=post_surname,
            #            cell=post_cell, email=post_email, userId=post_user_id)

            otp = generate_otp()

            user = User.objects.create_user(title=post_title, initials=post_initials, name=post_name, surname=post_surname,
                                            cell=post_cell, email=post_email, userId=post_user_id, password=otp)

            if not user:
                messages.add_message(request, messages.ERROR, "User could not be added")

            else:
                generate_email(otp, post_name, post_surname, post_email)

                post_status = user_form.cleaned_data['status']
                user.status = post_status
                user.save()
                print("created user")

                for roundObj in RoundDetail.objects.all():
                    team = TeamDetail(user=user, roundDetail=roundObj)
                    team.save()
            return HttpResponseRedirect("../")
    else:
        user_form = UserForm()
    return HttpResponseRedirect("../")