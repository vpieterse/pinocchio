import csv
import hashlib
import os
import random
import string
import time
import uuid

from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from .forms import DocumentForm, UserForm, LoginForm
from .models import Document
from .models import Question, RoundDetail, TeamDetail, Label, Response
from .models import Questionnaire, QuestionOrder
from .models import User


# Moved these views into seperate files
from .view.questionAdmin import question_admin, edit_question, save_question, delete_question
from .view.questionnaireAdmin import questionnaire_admin, edit_questionnaire, save_questionnaire, delete_questionnaire

def active_rounds(request):
    # TEST
    user = User.objects.get(userId='14035548')
    teams = TeamDetail.objects.filter(user=user).order_by('roundDetail__startingDate')
    exp_teams = TeamDetail.objects.filter(user=user and roundDetail.endingDate<datetime.date.now())
    context = {'teams': teams}
    return render(request, 'peer_review/activeRounds.html', context)


def team_members(request):
    # TEST
    user = User.objects.get(userId='14035548')
    rounds = RoundDetail.objects.all()
    team_list = []
    team_members = []
    for team in TeamDetail.objects.filter(user=user):
        teamName = team.teamName
        roundName = RoundDetail.objects.get(pk=team.roundDetail.pk).name
        team_list.append(team)
        for teamItem in TeamDetail.objects.filter(teamName=team.teamName):
            if teamItem.user != user:
                print(teamItem)
                team_members.append(teamItem)
    context = {'teams': team_list, 'members': team_members}
    print(team_list)
    print(team_members)
    return render(request, 'peer_review/teamMembers.html', context)


def account_details(request, user_id):
    user = User.objects.get(userId=user_id)
    context = {'user': user}
    return render(request, 'peer_review/accountDetails.html', context)


def login(request):
    logout(request)
    loginForm = LoginForm()
    context = {'loginForm': loginForm}
    return render(request, 'peer_review/login.html', context)


def auth(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    django_login(request, user)
                    return redirect('userAdmin')
        return redirect('/login/')
    else:
        return redirect('/login/')


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


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


def maintain_round(request):
    context = {'roundDetail': RoundDetail.objects.all(),
               'questionnaires': Questionnaire.objects.all()}
    return render(request, 'peer_review/maintainRound.html', context)


def maintain_team(request):
    if request.method == "POST":
        round_pk = request.POST.get("roundPk")

        context = {'users': User.objects.all(),
                   'rounds': RoundDetail.objects.all(),
                   'teams': TeamDetail.objects.all(),
                   'roundPk': round_pk}

    else:
        context = {'users': User.objects.all(),
                   'rounds': RoundDetail.objects.all(),
                   'teams': TeamDetail.objects.all(),
                   'roundPk': "none"}
    return render(request, 'peer_review/maintainTeam.html', context)


# def questionAdmin(request):
#     # print(request.user.is_authenticated())
#     # if not request.user.is_authenticated():
#     #     return render(request, "peer_review/login.html")

#     context = {'questions': getQuestions()}
#     return render(request, 'peer_review/questionAdmin.html', context)

def questionnaire(request, round_pk):
    # if request.method == "POST":
    user = User.objects.get(userId='14035548')  # TEST
    questionnaire = RoundDetail.objects.get(pk=round_pk).questionnaire
    q_orders = QuestionOrder.objects.filter(questionnaire=questionnaire)
    print(user)
    print(RoundDetail.objects.get(pk=round_pk))
    team_name = TeamDetail.objects.get(user=user, roundDetail=RoundDetail.objects.get(pk=round_pk)).teamName
    q_team = TeamDetail.objects.filter(roundDetail=RoundDetail.objects.get(pk=round_pk), teamName=team_name)

    reponses = Response.objects.filter(user=request.user, roundDetail=RoundDetail.objects.get(pk=round_pk))
    context = {'questionOrders': q_orders, 'teamMembers': q_team, 'questionnaire': questionnaire, 'currentUser': user,
               'round': round_pk}
    print(context)
    return render(request, 'peer_review/questionnaire.html', context)

    # else:
    #     return render(request, 'peer_review/userError.html')


def save_questionnaire_progress(request):
    if request.method == "POST":
        question = Question.objects.get(pk=request.POST.get('questionPk'))
        round_detail = RoundDetail.objects.get(pk=request.POST.get('roundPk'))
        user = request.user

        # If grouping == None, there is no label or subjectUser
        if question.questionGrouping.grouping == "None":
            label = None  # test
            subject_user = None  # test
        # If grouping == Label, there is a label but no subjectUser
        elif question.questionGrouping.grouping == "Label":
            label = Label.objects.get(pk=request.POST.get('label'))
            subject_user = None  # test
        # If grouping == Rest || All, there is a subjectUser but no label
        else:
            subject_user = User.objects.get(pk=request.POST.get('subjectUser'))
            label = None

        answer = request.POST.get('answer')
        Response.objects.create(question=question,
                                roundDetail=round_detail,
                                user=user,
                                subjectUser=subject_user,
                                label=label,
                                answer=answer)
        return JsonResponse({'result': 0})
    else:
        return JsonResponse({'result': 1})


def get_responses(request):
    question = Question.objects.get(pk=request.GET.get('questionPk'))
    round_detail = RoundDetail.objects.get(pk=request.GET.get('roundPk'))
    responses = Response.objects.filter(user=request.user, roundDetail=round_detail, question=question)

    # Need to find a way to get the latest responses, instead of all of them
    json = {'answers': [], 'labelOrUserIds': [], 'labelOrUserNames': []}
    for r in responses:
        json['answers'].append(r.answer)
        if question.questionGrouping.grouping == "Label":
            json['labelOrUserNames'].append(r.label.labelText)
            json['labelOrUserIds'].append(r.label.id)
        elif question.questionGrouping.grouping != "None":
            json['labelOrUserNames'].append(r.subjectUser.name + ' ' + r.subjectUser.surname)
            json['labelOrUserIds'].append(r.subjectUser.id)
    return JsonResponse(json)


# Commented out temporarily as there are three(?!) definitions of questionnaire and I have no idea which one is the right one -Jason
# @login_required
# def questionnaire(request, questionnairePk):
# 	if request.method == "POST":
#         #print(request.user.email)

# 		context = {'questionnaire': Questionnaire.objects.all(), 'questions' : Question.objects.all(),
# 			   'questionTypes' : QuestionType.objects.all(), 'questionOrder' : QuestionOrder.objects.all(),
# 			   'questionGrouping' : QuestionGrouping.objects.all(), 'questionnairePk' : int(questionnairePk),
#                'questionRanking' : Rank.objects.all(), 'questionChoices' : Choice.objects.all(),
#                'questionRating' : Rate.objects.all(), 'userDetails' : User.objects.all(),
#                'freeformDetails' : FreeformItem.objects.all(), 'questionLabels' : Label.objects.all(),
#                'roundDetails' : RoundDetail.objects.all(), 'teamDetails' : TeamDetail.objects.all(),
#                'userName' : request.user.email}
# 		return render(request, 'peer_review/questionnaire.html', context)
# 	else:
# 		return render(request, 'peer_review/userError.html')

# def questionnaire(request, questionnairePk):
# 	if request.method == "POST":
# 		context = {'questionnaire': Questionnaire.objects.all(), 'questions' : Question.objects.all(),
# 			   'questionTypes' : QuestionType.objects.all(), 'questionOrder' : QuestionOrder.objects.all(),
# 			   'questionGrouping' : QuestionGrouping.objects.all(), 'questionnairePk' : int(questionnairePk),
#                'questionRanking' : Rank.objects.all(), 'questionChoices' : Choice.objects.all(),
#                'questionRating' : Rate.objects.all(), 'userDetails' : User.objects.all(),
#                'freeformDetails' : FreeformItem.objects.all(), 'questionLabels' : Label.objects.all(),
#                'roundDetails' : RoundDetail.objects.all(), 'teamDetails' : TeamDetail.objects.all()}
# 		return render(request, 'peer_review/questionnaire.html', context)
# 	else:
# 		return render(request, 'peer_review/userError.html')

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


def user_error(request):
    return render(request, 'peer_review/userError.html')


@login_required
def user_list(request):
    users = User.objects.all
    user_form = UserForm()
    doc_form = DocumentForm()

    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir)
    file = open(file_path + '/text/email.txt', 'r+')
    email_text = file.read()
    file.close()

    return render(request, 'peer_review/userAdmin.html',
                  {'users': users, 'userForm': user_form, 'docForm': doc_form, 'email_text': email_text})


def get_teams(request):
    response = {}
    if request.method == "GET":
        teams = TeamDetail.objects.all()
        for team in teams:
            user = User.objects.get(pk=team.user.pk)
            response[team.pk] = {
                'userId': user.userId,
                'initials': team.user.initials,
                'surname': team.user.surname,
                'round': team.roundDetail.name,
                'team': team.teamName,
                'status': team.status,
                'teamId': team.pk,
            }
    elif request.method == "POST":
        user_pk = request.POST.get("pk")
        user = User.objects.get(pk=user_pk)

        teams = TeamDetail.objects.filter(user=user)
        for team in teams:
            response[team.pk] = {
                'round': team.roundDetail.name,
                'team': team.teamName,
                'status': team.status,
                'teamId': team.pk,
                'roundPk': team.roundDetail.pk
            }
    return JsonResponse(response)


def get_questionnaire_for_round(request, round_pk):
    round = RoundDetail.objects.get(pk=round_pk)
    if request.method == "GET":
        response = {
            'questionnaire': round.questionnaire.label
        }
    return JsonResponse(response)


def get_teams_for_round(request, round_pk):
    teams = TeamDetail.objects.filter(roundDetail_id=round_pk)
    response = {}
    for team in teams:
        response[team.pk] = {
            'userId': team.user.pk,
            'teamName': team.teamName,
            'status': team.status,
        }
    # print(response)
    return JsonResponse(response)


def change_user_team_for_round(request, round_pk, user_pk, team_name):
    try:
        team = TeamDetail.objects.filter(user_id=user_pk).get(roundDetail_id=round_pk)
    except TeamDetail.DoesNotExist:
        team = TeamDetail(
            user=User.objects.get(pk=user_pk),
            roundDetail=RoundDetail.objects.get(pk=round_pk)
        )
    team.teamName = team_name
    if team_name == 'emptyTeam':
        team.status = 'NA'
    team.save()
    return JsonResponse({'success': True})


def change_team_status(request, team_pk, status):
    team = TeamDetail.objects.get(pk=team_pk)
    team.status = status
    team.save()
    return JsonResponse({'success': True})


def generate_otp():
    n = random.randint(4, 10)
    otp = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
                  for _ in range(n))
    return otp


def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


def generate_email(otp, post_name, post_surname, email_text, email):
    fn = "{firstname}"
    ln = "{lastname}"
    otp = "{otp}"
    datetime = "{datetime}"
    login = "{login}"

    email_text = email_text.replace(fn, post_name)
    email_text = email_text.replace(ln, post_surname)
    email_text = email_text.replace(otp, otp)
    email_text = email_text.replace(datetime, time.strftime("%H:%M:%S %d/%m/%Y"))
    email_text = email_text.replace(login, email)

    print(email_text)

    # send_mail(email_subject, email_text, 'no-reply@pinocchio.up.ac.za', [email], fail_silently=False)


def submit_form(request):
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

            user = User(title=post_title, initials=post_initials, name=post_name, surname=post_surname,
                        cell=post_cell, email=post_email, userId=post_user_id)

            otp = generate_otp()

            module_dir = os.path.dirname(__file__)
            file_path = os.path.join(module_dir)
            file = open(file_path + '/text/email.txt', 'a+')
            file.seek(0)
            email_text = file.read()
            file.close()

            generate_email(otp, post_name, post_surname, email_text, post_email)
            post_password = otp  # hash_password(otp)

            post_status = user_form.cleaned_data['status']

            user.password = post_password
            user.status = post_status
            user.save()

            for roundObj in RoundDetail.objects.all():
                team = TeamDetail(user=user, roundDetail=roundObj)
                team.save()

            return HttpResponseRedirect("../")
    else:
        user_form = UserForm()
    return HttpResponseRedirect("../")


def get_user(request, user_pk):
    response = {}
    if request.method == "GET":
        user = User.objects.get(pk=user_pk)
        response = {
            'userId': user.userId,
            'name': user.name,
            'surname': user.surname
        }
    return JsonResponse(response)


def user_profile(request, user_pk):
    if request.method == "GET":
        user = User.objects.get(pk=user_pk)
    # TODO Add else
    return render(request, 'peer_review/userProfile.html', {'user': user})


def user_delete(request):
    if request.method == "POST":
        to_delete = request.POST.getlist("toDelete[]")

        for userPk in to_delete:
            user = User.objects.get(pk=userPk)

            user.delete()

    return HttpResponseRedirect('../')


def user_update(request, user_pk):
    if request.method == "POST":
        user = User.objects.get(pk=user_pk)

        post_user_id = request.POST.get("userId")
        post_title = request.POST.get("title")
        post_initials = request.POST.get("initials")
        post_name = request.POST.get("name")
        post_surname = request.POST.get("surname")
        post_cell = request.POST.get("cell")
        post_email = request.POST.get("email")
        post_status = request.POST.get("status")

        user.userId = post_user_id
        user.status = post_status
        user.title = post_title
        user.initials = post_initials
        user.name = post_name
        user.surname = post_surname
        user.cell = post_cell
        user.email = post_email

        user.save()
    return HttpResponseRedirect('../')


def reset_password(request, user_pk):
    if request.method == "POST":
        user = User.objects.get(pk=user_pk)

        otp = generate_otp()
        generate_email(otp, user.name, user.surname)
        password = hash_password(otp)

        user.password = password
        user.save()

        print(otp)
        print(password)
        print(check_password(password, otp))
        return HttpResponseRedirect('../')


def add_csv_info(user_list):
    for row in user_list:
        otp = generate_otp()
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir)
        file = open(file_path + '/text/email.txt', 'a+')
        file.seek(0)
        email_text = file.read()
        file.close()

        generate_email(otp, row['name'], row['surname'], email_text, row['email'])
        password = hash_password(otp)

        user = User(userId=row['user_id'], password=password, status=row['status'], title=row['title'],
                    initials=row['initials'], name=row['name'], surname=row['surname'],
                    cell=row['cell'], email=row['email'])

        user.save()
    return  # todo return render request


def submit_csv(request):
    global errortype
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            file_path = newdoc.docfile.url
            file_path = file_path[1:]

            user_list = list()
            error = False

            documents = Document.objects.all()

            count = 0
            with open(file_path) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    valid = validate(row)
                    count += 1
                    if valid == 1:
                        # title = row['title']
                        # initials = row['initials']
                        # name = row['name']
                        # surname = row['surname']
                        # email = row['email']
                        # cell = row['cell']
                        #
                        # userId = row['user_id']
                        # status = row['status']
                        # OTP = generate_OTP()
                        # generate_email(OTP, name, surname)
                        # password = hash_password(OTP)

                        user_list.append(row)
                        # ToDo check for errors in multiple rows
                    else:
                        error = True
                        if valid == 0:
                            message = "Oops! Something seems to be wrong with the CSV file."
                            errortype = "Incorrect number of fields."
                            return render(request, 'peer_review/csvError.html',
                                          {'message': message, 'error': errortype})
                        else:
                            message = "Oops! Something seems to be wrong with the CSV file at row " + str(count) + "."

                            rowlist = list()
                            rowlist.append(row['title'])
                            rowlist.append(row['initials'])
                            rowlist.append(row['name'])
                            rowlist.append(row['surname'])
                            rowlist.append(row['email'])
                            rowlist.append(row['cell'])
                            rowlist.append(row['user_id'])
                            rowlist.append(row['status'])

                        if valid == 2:
                            errortype = "Not all fields contain values."
                        if valid == 3:
                            errortype = "Cell or user ID is not a number."
                        if valid == 4:
                            errortype = "User already exists."

                        csvfile.close()

                        if os.path.isfile(file_path):
                            os.remove(file_path)

                        return render(request, 'peer_review/csvError.html',
                                      {'message': message, 'row': rowlist, 'error': errortype})
        else:
            form = DocumentForm()
            message = "Oops! Something seems to be wrong with the CSV file."
            errortype = "No file selected."
            return render(request, 'peer_review/csvError.html', {'message': message, 'error': errortype})

        if not (error):
            add_csv_info(user_list)

    if os.path.isfile(file_path):
        os.remove(file_path)
    return HttpResponseRedirect('../')


def validate(row):
    # 0 = incorrect number of fields
    # 1 = correct
    # 2 = missing value/s
    # 3 = incorrect format
    # 4 = user already exists

    if len(row) < 8:
        return 0

    for key, value in row.items():
        if value is None:
            return 2

    for key, value in row.items():
        if key == "cell" or key == "user_id":
            try:
                int(value)
            except ValueError:
                return 3

    user = User.objects.filter(userId=row['user_id'])

    if user.count() > 0:
        return 4

    return 1


def write_dump(round_pk):
    data = [['roundId', 'qId', 'q', 'answer'],
            ['x', 'x', 'x', 'x'],
            ['y', 'y', 'y', 'y']]

    with open('media/dumps/' + round_pk + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(data)

    csvfile.close()


def round_dump(request):
    if request.method == "POST":
        roundPk = request.POST.get("roundPk")
        write_dump(roundPk)
    return HttpResponse()


def update_email(request):
    if request.method == "POST":
        email_text = request.POST.get("emailText")

        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir)
        file = open(file_path + '/text/email.txt', 'w+')

        file.write(email_text)
        file.close()
    return HttpResponseRedirect('../')


def add_team_csv_info(team_list):
    for row in team_list:
        user_det_id = User.objects.get(userId=row['userID']).pk
        round_det_id = RoundDetail.objects.get(name=row['roundDetail']).pk
        change_user_team_for_round("", round_det_id, user_det_id, row['teamName'])
    return 1


def submit_team_csv(request):
    global errortype
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        file_path = newdoc.docfile.url
        file_path = file_path[1:]

        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            team_list = list()
            error = False

            documents = Document.objects.all()

            count = 0
            with open(file_path) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    count += 1
                    valid = validate_team_csv(row)
                    if valid == 0:
                        print(row['userID'])
                        team_list.append(row)
                    else:
                        error = True
                        message = "Oops! Something seems to be wrong with the CSV file at row " + str(count) + "."

                        row_list = list()
                        row_list.append(row['userID'])
                        row_list.append(row['roundDetail'])
                        row_list.append(row['teamName'])

                        if valid == 1:
                            errortype = "Incorrect number of fields."
                        elif valid == 2:
                            errortype = "Not all fields contain values."
                        elif valid == 3:
                            errortype = "user ID is not a number."

                        os.remove(file_path)
                        return render(request, 'peer_review/csvError.html',
                                      {'message': message, 'row': row_list, 'error': errortype})
        else:
            form = DocumentForm()
            message = "Oops! Something seems to be wrong with the CSV file."
            errortype = "No file selected."
            os.remove(file_path)
            return render(request, 'peer_review/csvError.html', {'message': message, 'error': errortype})

        if not error:
            add_team_csv_info(team_list)
    os.remove(file_path)
    return HttpResponseRedirect('../')


def validate_team_csv(row):
    # 0 = correct
    # 1 = incorrect number of fields
    # 2 = missing value/s
    # 3 = incorrect format

    if len(row) != 3:
        return 1
    for key, value in row.items():
        if value is None:
            return 2
        if key == "userID":
            try:
                int(value)
            except ValueError:
                return 3
    return 0


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
            post_description = request.POST.get("desc")
            post_questionnaire = request.POST.get("questionn")
            post_name = request.POST.get("Roundname")
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
