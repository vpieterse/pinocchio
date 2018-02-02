import random
import string

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from peer_review.decorators.userRequired import user_required

from peer_review.email import generate_otp_email
from peer_review.forms import ResetForm, UserForm
from peer_review.models import User
from peer_review.decorators.adminRequired import admin_required, admin_required_test
from django.http import HttpResponse


def forgot_password(request):
    reset_form = ResetForm()
    context = {'resetForm': reset_form}
    return render(request, 'peer_review/forgotPassword.html', context)


def generate_otp():
    n = random.randint(4, 10)
    otp = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
                  for _ in range(n))
    return otp


# Creates a new user, sends a confirmation OTP email and returns the newly created user
def create_user_send_otp(user_title,
                         user_initials,
                         user_name,
                         user_surname,
                         user_cell,
                         user_email,
                         user_user_id,
                         user_status):
    otp = generate_otp()
    user = User.objects.create_user(title=user_title,
                                    initials=user_initials,
                                    name=user_name,
                                    surname=user_surname,
                                    cell=user_cell,
                                    email=user_email,
                                    user_id=user_user_id,
                                    password=otp,
                                    status=user_status)

    if user:
        generate_otp_email(otp, user_name, user_surname, user_email, user_user_id)
        user.save()

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
            post_user_id = user_form.cleaned_data['user_id']
            post_status = user_form.cleaned_data['status']

            # user = User(title=post_title, initials=post_initials, name=post_name, surname=post_surname,
            #            cell=post_cell, email=post_email, userId=post_user_id)

            user = create_user_send_otp(user_title=post_title, user_initials=post_initials, user_name=post_name,
                                        user_surname=post_surname, user_cell=post_cell, user_user_id=post_user_id,
                                        user_email=post_email, user_status=post_status)
            if not user:
                messages.add_message(request, messages.ERROR, "User could not be added")
            else:
                messages.add_message(request, messages.SUCCESS, "User added successfully")

            return HttpResponseRedirect("/userAdmin")
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 "Form filled in incorrectly or username/email is already in use")
    else:
        UserForm()
    return HttpResponseRedirect("/userAdmin")


@user_required
def user_update(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, pk=user_id)
        if request.user == user or admin_required_test(request.user):
            post_title = request.POST.get("title")
            post_initials = request.POST.get("initials")
            post_name = request.POST.get("name")
            post_surname = request.POST.get("surname")
            post_cell = request.POST.get("cell")
            post_email = request.POST.get("email")
            if admin_required_test(request.user):
                post_status = request.POST.get("status")
                user.status = post_status

            user.title = post_title
            user.initials = post_initials
            user.name = post_name
            user.surname = post_surname
            user.cell = post_cell
            user.email = post_email
            print("updating user")
            user.save()
            return HttpResponse()
    return redirect('/login/')
