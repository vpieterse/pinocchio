import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from peer_review.decorators.adminRequired import admin_required
from peer_review.forms import RecoverPasswordForm
from peer_review.view.userFunctions import unsign_user_id, sign_user_id
from .forms import DocumentForm, UserForm, LoginForm
from .models import Questionnaire
from .models import RoundDetail, TeamDetail
from .models import User
from .view.userFunctions import user_error


# Moved these views into separate files
# def forgot_password(request):
#     resetForm = ResetForm()
#     context = {'resetForm': resetForm}
#     return render(request, 'peer_review/forgotPassword.html', context)
# def active_rounds(request):
#     if not request.user.is_authenticated():
#         return user_error(request)


def login(request):
    logout(request)
    login_form = LoginForm()
    context = {'loginForm': login_form}
    return render(request, 'peer_review/login.html', context)


def auth(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_id = request.POST.get('userName')
            password = request.POST.get('password')
            user = authenticate(user_id=user_id, password=password)
            if user:
                if user.is_active:
                    # Redirect if OTP is set
                    if User.objects.get(user_id=user_id).OTP:
                        request.user = user
                        return change_password(request)
                    # return change_password_request(request, user_id, password)
                    django_login(request, user)
                    # Redirect based on user account type
                    if user.is_staff or user.is_superuser:
                        return redirect('userAdmin')
                    else:
                        return redirect('activeRounds')
        # Access Denied
        messages.add_message(request, messages.ERROR, "Incorrect username or password")
        return redirect('/login/')
    else:
        return redirect('/login/')


"""
When a user clicks on the link they get per email about
resetting their password, the request is sent to this
handler to change their password. Since the URL token
is signed by the server, we can safely assume that the
user requesting this page is the real user. However,
they are not logged in; this page only allows for
changing their password.
"""


def recover_password(request, key):
    if request.method == 'GET':
        # Test if the key is still valid
        user_id = unsign_user_id(key, settings.FORGOT_PASSWORD_AGE)
        if not user_id:
            messages.error(request, 'The link has expired or is invalid. Please generate a new one.')
            return redirect('forgotPassword')

        context = {}

        try:
            user = User.objects.get(user_id=user_id)
            context['name'] = user.name
            context['surname'] = user.surname

        except Exception as e:
            print(e)

        form = RecoverPasswordForm(request.user, url_token=key)
        context['form'] = form
        return render(request, 'peer_review/forgotPasswordChange.html', context)

    if request.method == 'POST':
        new_form = RecoverPasswordForm(request.user, None, request.POST)
        new_form.full_clean()
        key = new_form.cleaned_data['urlTokenField']
        for err, description in new_form.errors.items():
            messages.error(request, description)

        # If the form is valid, go ahead and change the user's password.
        if new_form.is_valid():
            try:
                user_id = unsign_user_id(key, settings.FORGOT_PASSWORD_AGE)
                if not user_id:
                    messages.error(request, 'The link has expired or is invalid. Please generate a new one.')
                    return redirect('forgotPassword')

                user = User.objects.get(user_id=user_id)
                user.set_password(new_form.cleaned_data['new_password1'])
                user.OTP = False
                user.save()
                messages.success(request, "Success! Please log in with your new password")
                return redirect("login")

            except User.DoesNotExist:
                messages.error(request, "Your username seems to be invalid. This is not supposed to happen. "
                                        + "Please contact admin if problem persists.")
                return redirect("login")

            except Exception as e:
                print(e)
                messages.error(request, "There was a problem changing your password. Please try again.")
                return redirect("forgotPassword")

        return redirect('recoverPassword', key=key)


def change_password(request):
    user = request.user
    key = sign_user_id(user.user_id)
    request.method = 'GET'
    return recover_password(request, key)


def index(request):
    return login(request)


@admin_required
def get_questionnaire_for_team(request):
    if request.method == "POST":
        team = get_object_or_404(TeamDetail, pk=request.POST.get("teamPk"))
        user = get_object_or_404(User, pk=team.user.pk)
        current_questionnaire = get_object_or_404(Questionnaire, pk=team.roundDetail.questionnaire.pk)
        # TODO if team progress exists...
        context = {'team': team, 'user': user, 'questionnaire': current_questionnaire}
        return render(request, 'peer_review/questionnaireTest.html', context)
    else:
        return redirect('accountDetails')


@admin_required
def user_list(request):
    users = User.objects.all
    user_form = UserForm()
    doc_form = DocumentForm()

    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir)
    file = open(file_path + '/text/otp_email.txt', 'r+')
    email_text = file.read()
    file.close()

    reset_link = '/recoverPassword/' + sign_user_id(request.user.user_id)
    return render(request, 'peer_review/userAdmin.html',
                  {'users': users, 'userForm': user_form, 'docForm': doc_form, 'email_text': email_text,
                   'reset_link': reset_link})


@admin_required()
def get_questionnaire_for_round(request, round_pk):
    current_round = RoundDetail.objects.get(pk=round_pk)
    response = {}
    if request.method == "GET":
        response = {
            'questionnaire': current_round.questionnaire.label
        }
    return JsonResponse(response)


@admin_required
def get_user(request, user_id):
    if not request.user.is_authenticated():
        return user_error(request)

    response = {}
    if request.method == "GET":
        user = get_object_or_404(User, pk=user_id)
        response = {
            'user_id': user.user_id,
            'name': user.name,
            'surname': user.surname
        }
    return JsonResponse(response)


@admin_required
def user_profile(request, user_id):
    if request.method == "GET":
        user = get_object_or_404(User, pk=user_id)
        return render(request, 'peer_review/userProfile.html', {'user': user})
    else:
        messages.success(request, "Something went wrong while trying to view the user profile")
        return HttpResponseRedirect('../')


@admin_required
def user_delete(request):
    if request.method == "POST":
        to_delete = request.POST.getlist("toDelete[]")

        for userPk in to_delete:
            user = get_object_or_404(User, pk=userPk)

            user.delete()

    return HttpResponseRedirect('../')


@admin_required
def update_email(request):
    if request.method == "POST":
        email_text = request.POST.get("emailText")

        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir)
        file = open(file_path + '/text/otp_email.txt', 'w+')

        file.write(email_text)
        file.close()
    return HttpResponseRedirect('../')


# Create a response
# {respondent_pk, labelPk/userPk, roundPk, answer, questionPk}
# @user_required
# def create_response(request):
    # if 'labelPk' in request.POST:
    #     target = request.POST['labelPk']
    # else:
    #     target = request.POST['userPk']

#    question = Question.objects.get(pk=request.POST['questionPk'])
#    round_detail = RoundDetail.objects.get(pk=request.POST['roundPk'])
#    user = User.objects.get(pk=request.POST['respondent_pk'])
#    other_user = User.objects.get(pk=request.POST['userPk'])
#    label = Label.objects.get(pk=labelPk)
#
#    Response.objects.create(question=question,
#                            roundDetail=round_detail,
#                            user=user,
#                            otherUser=other_user,
#                            label=label,
#                            answer=answer)
#    return HttpResponse()


@admin_required
def report(request):
    if request.method == "POST":
        round_pk = request.POST.get("roundPk")
        context = {
            "roundPk": round_pk,
            "rounds": RoundDetail.objects.all()
        }
    else:
        context = {
            "roundPk": "",
            "rounds": RoundDetail.objects.all()
        }
    return render(request, 'peer_review/report.html', context)
