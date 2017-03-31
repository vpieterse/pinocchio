from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from peer_review.email import generate_otp_email
from peer_review.forms import ResetForm, UserForm
from peer_review.generate_otp import generate_otp
from peer_review.models import User, RoundDetail, TeamDetail
from peer_review.decorators.adminRequired import admin_required


def forgot_password(request):
    reset_form = ResetForm()
    context = {'resetForm': reset_form}
    return render(request, 'peer_review/forgotPassword.html', context)


# Creates a new user, sends a confirmation OTP email and returns the newly created user
def create_user_send_otp(user_title, user_initials, user_name, user_surname, user_cell, user_email, user_userId, user_status):
    otp = generate_otp()
    user = User.objects.create_user(title=user_title, initials=user_initials, name=user_name, surname=user_surname,
                                    cell=user_cell, email=user_email, userId=user_userId, password=otp, status=user_status)

    if user:
        generate_otp_email(otp, user_name, user_surname, user_email, user_userId)
        user.save()

        for roundObj in RoundDetail.objects.all():
            team = TeamDetail(user=user, roundDetail=roundObj)
            team.save()

    return user

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
            post_status = user_form.cleaned_data['status']

            # user = User(title=post_title, initials=post_initials, name=post_name, surname=post_surname,
            #            cell=post_cell, email=post_email, userId=post_user_id)


            user = create_user_send_otp(user_title=post_title, user_initials=post_initials, user_name=post_name,
                                        user_surname=post_surname, user_cell=post_cell, user_userId=post_user_id,
                                        user_email=post_email, user_status=post_status)
            if not user:
                messages.add_message(request, messages.ERROR, "User could not be added")
            else:
                messages.add_message(request, messages.SUCCESS, "User added successfully")

            return HttpResponseRedirect("/userAdmin")
        else:
            messages.add_message(request, messages.ERROR, "Form filled in incorrectly or username/email is already in use")
    else:
        user_form = UserForm()
    return HttpResponseRedirect("/userAdmin")