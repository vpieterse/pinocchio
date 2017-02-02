import csv
import os
import time
import mimetypes

from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from wsgiref.util import FileWrapper

from peer_review.decorators.adminRequired import admin_required
from peer_review.decorators.userRequired import user_required
from peer_review.view.userFunctions import unsign_userId
from .forms import DocumentForm, UserForm, LoginForm, ResetForm
from .models import Document
from .models import Question, RoundDetail, TeamDetail, Label, Response
from .models import Questionnaire, QuestionOrder
from .models import User

# Moved these views into seperate files
from peer_review.email import generate_otp_email
from peer_review.passwordUtility import generate_otp
from peer_review.passwordUtility import hash_password
from .view.questionAdmin import question_admin, edit_question, save_question, delete_question
from .view.questionnaireAdmin import questionnaire_admin, questionnaire_preview, edit_questionnaire, save_questionnaire, delete_questionnaire
from .view.maintainTeam import maintain_team, change_team_status, change_user_team_for_round, get_teams_for_round, get_teams, submit_team_csv

from .view.questionnaire import questionnaire, save_questionnaire_progress, get_responses
from .view.userAdmin import add_csv_info, submit_csv

def active_rounds(request):
    if not request.user.is_authenticated():
        return user_error(request)


from .view.userAdmin import add_csv_info, submit_csv
from .view.userManagement import forgot_password
from .view.userFunctions import account_details, active_rounds, get_team_members, reset_password, user_error, user_reset_password
from .view.roundManagement import maintain_round


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
            user = authenticate(userId=user_id, password=password)
            if user:
                if user.is_active:
                    # Redirect if OTP is set
                    # if User.objects.get(userId=user_id).OTP:
                    #     return change_password(request, user_id, password)
                    django_login(request, user)
                    # Redirect based on user account type
                    if user.is_staff or user.is_superuser:
                        return redirect('userAdmin')
                    else:
                        return redirect('activeRounds')
        # Access Denied
        messages.add_message(request, messages.ERROR, "Incorrect username or password")
        return redirect('/login/')

    elif request.method == 'GET' and request.GET.get('key', None):

        """
        Reset password one time link redirects to this page with a GET request
        and a token in the URL query string 'key'
        """
        key = request.GET.get('key')
        userId = unsign_userId(key)
        print(userId)
        return redirect('/login/')

    else:
        return redirect('/login/')


def change_password(request, user_id, password):
    user = authenticate(userId=user_id, password=password)
    if user:
        context = {}
        return render(request, '/peer_review/setPassword.html/', context)
    else:
        messages.add_message(request, messages.ERROR, "Incorrect username or password")
        return redirect('/login/')


def index(request):
    return login(request)


def file_upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            new_doc = Document(docfile=request.FILES['docfile'])
            new_doc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect('')
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'peer_review/fileUpload.html',
        {'documents': documents, 'form': form}
        , context_instance=RequestContext(request)
    )


def get_questionnaire_for_team(request):
    if request.method == "POST":
        # TEST
        team = TeamDetail.objects.get(pk=request.POST.get("teamPk"))
        user = User.objects.get(pk=team.user.pk)
        questionnaire = Questionnaire.objects.get(pk=team.roundDetail.questionnaire.pk)
        # TODO if team progress exists...
        context = {'team': team, 'user': user, 'questionnaire': questionnaire}
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

    return render(request, 'peer_review/userAdmin.html',
                  {'users': users, 'userForm': user_form, 'docForm': doc_form, 'email_text': email_text})


def get_questionnaire_for_round(request, round_pk):
    round = RoundDetail.objects.get(pk=round_pk)
    response = {}
    if request.method == "GET":
        response = {
            'questionnaire': round.questionnaire.label
        }
    return JsonResponse(response)


def get_user(request, userId):
    if not request.user.is_authenticated():
        return user_error(request)

    response = {}
    if request.method == "GET":
        user = User.objects.get(pk=userId)
        response = {
            'userId': user.userId,
            'name': user.name,
            'surname': user.surname
        }
    return JsonResponse(response)

@user_required
def user_profile(request, userId):
    if request.method == "GET":
        user = User.objects.get(pk=userId)
    # TODO Add else
    return render(request, 'peer_review/userProfile.html', {'user': user})


def user_delete(request):
    if request.method == "POST":
        to_delete = request.POST.getlist("toDelete[]")

        for userPk in to_delete:
            user = User.objects.get(pk=userPk)

            user.delete()

    return HttpResponseRedirect('../')


def user_update(request, userId):
    if request.method == "POST":
        user = User.objects.get(pk=userId)

        post_title = request.POST.get("title")
        post_initials = request.POST.get("initials")
        post_name = request.POST.get("name")
        post_surname = request.POST.get("surname")
        post_cell = request.POST.get("cell")
        post_email = request.POST.get("email")
        post_status = request.POST.get("status")

        user.status = post_status
        user.title = post_title
        user.initials = post_initials
        user.name = post_name
        user.surname = post_surname
        user.cell = post_cell
        user.email = post_email

        user.save()
    return HttpResponseRedirect('../')



def write_dump(round_pk):
    dump_file = 'media/dumps/' + str(round_pk) + '.csv'
    data = [['ROUND ID:', round_pk],
            ['DUMP DATE:', time.strftime("%d/%m/%Y %H:%M:%S")], [''],
            ['QUESTION', 'ANSWER', 'USERID']]
    
    roundData = Response.objects.filter(roundDetail=round_pk)
    
    if len(roundData) > 0:
        for item in roundData:
            data.append([item.question.questionText, item.answer, item.user.userId])
    else:
        data.append(['NO DATA'])

    with open(dump_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(data)

    csvfile.close()
    return str(dump_file) # Returns dump filename


def round_dump(request):
    if request.method == "POST":
        roundPk = request.POST.get("roundPk")
        dump_file = write_dump(roundPk)
        # Download Dump
        wrapper = FileWrapper(open(dump_file))
        content_type = mimetypes.guess_type(dump_file)[0]
        print(content_type)
        response = HttpResponse(wrapper,content_type=content_type)
        #response['Content-Length'] = os.path.getsize(dump_file)    
        response['Content-Disposition'] = "attachment; filename=dump-r" + str(roundPk) + ".csv"
        return response


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


def round_delete(request, round_pk):
    round = RoundDetail.objects.get(pk=round_pk)
    round.delete()
    return HttpResponseRedirect('../')


def round_update(request, round_pk):
    try:
        if request.method == "POST":
            round = RoundDetail.objects.get(pk=round_pk)

            post_starting_date = request.POST.get("startingDate")
            post_description = request.POST.get("description")
            post_questionnaire = request.POST.get("questionnaire")
            post_name = request.POST.get("roundName")
            post_ending_date = request.POST.get("endingDate")
            round.description = post_description
            round.questionnaire = Questionnaire.objects.get(pk=post_questionnaire)
            round.name = post_name
            round.startingDate = post_starting_date
            round.endingDate = post_ending_date
            round.save()
        return HttpResponseRedirect('../')
    except:
        return HttpResponseRedirect('../1')


# Create a round
def create_round(request):
    try:

        if 'description' in request.GET:
            r_description = request.GET['description']
            try:
                r_questionnaire = Questionnaire.objects.get(pk=request.GET['questionnaire'])
            except Questionnaire.DoesNotExist:
                r_questionnaire = None
            r_starting_date = request.GET['startingDate']
            r_ending_date = request.GET['endingDate']
            r_name = request.GET['name']
            r = RoundDetail(description=r_description,
                            questionnaire=r_questionnaire,
                            startingDate=r_starting_date,
                            name=r_name,
                            endingDate=r_ending_date,
                            )
            r.save()
        return HttpResponseRedirect('../maintainRound')
    except:
        return HttpResponseRedirect('../maintainRound/1')


def maintain_round_with_error(request, error):
    print(error)
    if error == '1':  # Incorrect Date format
        str_error = "Incorrect Date Format yyyy-mm-dd hh"
    else:
        str_error = "Unknown Error"

    context = {'roundDetail': RoundDetail.objects.all(),
               'questionnaires': Questionnaire.objects.all(),
               'error': str_error,}
    return render(request, 'peer_review/maintainRound.html', context)


# Create a response
# {responsdentPk, labelPk/userPk, roundPk, answer, questionPk}
def create_response(request):
    if 'labelPk' in request.POST:
        target = request.POST['labelPk']
    else:
        target = request.POST['userPk']

    question = Question.objects.get(pk=request.POST['questionPk'])
    round_detail = RoundDetail.objects.get(pk=request.POST['roundPk'])
    user = User.objects.get(pk=request.POST['responsdentPk'])
    other_user = User.objects.get(pk=request.POST['userPk'])
    label = Label.objects.get(pk=labelPk)

    Response.objects.create(question=question,
                            roundDetail=round_detail,
                            user=user,
                            otherUser=other_user,
                            label=label,
                            answer=answer)
    return HttpResponse()


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
