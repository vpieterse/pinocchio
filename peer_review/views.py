import csv
import os
import time
import mimetypes
from wsgiref.util import FileWrapper

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout
from django.db.models.aggregates import Max
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from peer_review.decorators.adminRequired import admin_required
from peer_review.forms import RecoverPasswordForm
from peer_review.view.userFunctions import unsign_user_id, sign_user_id
from .forms import DocumentForm, UserForm, LoginForm
from .models import RoundDetail, TeamDetail, Response
from .models import Questionnaire
from .models import User


# Moved these views into separate files

# def forgot_password(request):
#     resetForm = ResetForm()
#     context = {'resetForm': resetForm}
#     return render(request, 'peer_review/forgotPassword.html', context)
# def active_rounds(request):
#     if not request.user.is_authenticated():
#         return user_error(request)


from .view.userFunctions import user_error


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


def write_dump(round_pk):

    current_round = RoundDetail.objects.get(id=round_pk)
    dump_file = 'media/dumps/' + time.strftime("%Y-%m-%d %H:%M:%S") + 'round_' + str(current_round.name) + '.csv'
    data = [['ResponseID', 'Respondent', 'QuestionTitle', 'LabelTitle', 'SubjectUser', 'Answer']]

    # First, find the row id of the most recent answer to each question
    distinct_responses = Response.objects.filter(roundDetail=round_pk).values(
        "question_id", "user_id", "label_id", "subjectUser_id").annotate(max_id=Max('id'))

    # Filter response id's
    distinct_response_ids = [x['max_id'] for x in distinct_responses]

    # Fetch the most recent responses separately
    round_data = Response.objects.filter(id__in=distinct_response_ids).order_by(
        "user_id", "question_id", "label_id", "subjectUser_id")
    distinct_round_data = round_data.values('user_id', 'question_id', 'label_id', 'subjectUser_id', 'id')

    if len(distinct_round_data) > 0:
        for item_id in distinct_round_data:
            item = round_data.get(id=item_id['id'])
            response_id = item.id
            user_id = item.user.user_id
            question_label = item.question.questionLabel
            label = item.label

            subject_id = ""
            if item.subjectUser:
                subject_id = item.subjectUser.user_id
            answer = item.answer

            data.append([response_id, user_id, question_label, label, subject_id, answer])
    else:
        data.append(['NO DATA'])

    os.makedirs(os.path.dirname(dump_file), exist_ok=True)
    with open(dump_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_ALL)
        writer.writerows(data)

    csv_file.close()
    return str(dump_file)  # Returns dump filename


@admin_required
def round_dump(request):
    if request.method == "POST":
        round_pk = request.POST.get("roundPk")
        dump_file = write_dump(round_pk)
        # Download Dump
        wrapper = FileWrapper(open(dump_file))
        content_type = mimetypes.guess_type(dump_file)[0]
        response = HttpResponse(wrapper, content_type=content_type)
        current_round = get_object_or_404(RoundDetail, id=round_pk)
        # response['Content-Length'] = os.path.getsize(dump_file)
        response['Content-Disposition'] = "attachment; filename=" + time.strftime("%Y-%m-%d %H.%M.%S") \
                                          + ' round_' + current_round.name + ".csv"
        return response
    return user_error(request)


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


def get_type_id(question_type):
    # -1 = Error
    # 1 = Choice
    # 2 = Rank
    # 3 = Label
    # 4 = Rate
    # 5 = Freeform

    if question_type == "Choice":
        return 1
    elif question_type == "Rank":
        return 2
    elif question_type == "Label":
        return 3
    elif question_type == "Rate":
        return 4
    elif question_type == "Freeform":
        return 5
    else:
        return -1


def get_group_id(question_group):
    # -1 = Error
    # 1 = None
    # 2 = Rest
    # 3 = All

    if question_group == "None":
        return 1
    elif question_group == "Rest":
        return 2
    elif question_group == "All":
        return 3
    else:
        return -1


@admin_required
def round_delete(request):
    if request.method == "POST":
        current_round = get_object_or_404(RoundDetail, pk=request.POST.get("pk"))
        current_round.delete()
    return HttpResponseRedirect('../')


@admin_required
def round_update(request, round_pk):
    try:
        if request.method == "POST":
            current_round = get_object_or_404(RoundDetail, pk=round_pk)

            post_starting_date = request.POST.get("startingDate")
            post_description = request.POST.get("description")
            post_questionnaire = request.POST.get("questionnaire")
            post_name = request.POST.get("roundName")
            post_ending_date = request.POST.get("endingDate")
            current_round.description = post_description
            current_round.questionnaire = Questionnaire.objects.get(pk=post_questionnaire)
            current_round.name = post_name
            current_round.startingDate = post_starting_date
            current_round.endingDate = post_ending_date
            current_round.save()
        return HttpResponseRedirect('../')
    except Questionnaire.DoesNotExist:
        return HttpResponseRedirect('../1')


# Create a round
@admin_required
def create_round(request):
    try:

        if 'description' in request.GET:
            round_description = request.GET['description']
            try:
                round_questionnaire = Questionnaire.objects.get(pk=request.GET['questionnaire'])
            except Questionnaire.DoesNotExist:
                round_questionnaire = None
            round_starting_date = request.GET['startingDate']
            round_ending_date = request.GET['endingDate']
            round_name = request.GET['name']
            current_round = RoundDetail(description=round_description,
                                        questionnaire=round_questionnaire,
                                        startingDate=round_starting_date,
                                        name=round_name,
                                        endingDate=round_ending_date,
                                        )
            current_round.save()
        return HttpResponseRedirect('../maintainRound')
    except ValueError:
        return HttpResponseRedirect('../maintainRound/1')


@admin_required
def maintain_round_with_error(request, error):
    if error == '1':  # Incorrect Date format
        str_error = "Incorrect Date Format yyyy-mm-dd hh"
    else:
        str_error = "Unknown Error"

    context = {'roundDetail': RoundDetail.objects.all(),
               'questionnaires': Questionnaire.objects.all(),
               'error': str_error}
    return render(request, 'peer_review/maintainRound.html', context)

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
