from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http import JsonResponse
from django.core.mail import send_mail
import random
import string
import hashlib
import uuid

import time
import csv
import os

from django.utils import timezone

from .models import Document
from .models import Question, QuestionType, QuestionGrouping, Choice, Rank, Questionnaire, RoundDetail, TeamDetail, FreeformItem, Rate, Label
from .models import User, UserDetail
from .models import Questionnaire, QuestionOrder
from .forms import DocumentForm, UserForm, LoginForm

def activeRounds(request):
    rounds = RoundDetail.objects.all()
    context = {'rounds': rounds}
    return render(request, 'peer_review/activeRounds.html',context)
    
def teamMembers(request):
    #TEST
    user = User.objects.get(userId = '14031145')
    rounds = RoundDetail.objects.all()
    teamList = list()
    teamMembers = list()
    for team in TeamDetail.objects.all():
        if team.userDetail == user.userDetail:
            teamList.append(team)
    for team in teamList:
        for teamItem in TeamDetail.objects.all():
            if team.teamName == teamItem.teamName and team.roundDetail == teamItem.roundDetail and team.userDetail != teamItem.userDetail:
                teamMembers.append(teamItem)
    context = {'rounds': rounds, 'teamMembers': teamMembers}
    return render(request, 'peer_review/teamMembers.html',context)
    
def accountDetails(request):
    context = {}
    return render(request, 'peer_review/accountDetails.html',context)

def login(request):
    loginForm = LoginForm()
    context = {'loginForm': loginForm}
    return render(request, 'peer_review/login.html',context)

def auth(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            userType = form.cleaned_data['userType']
            if userType == 'A':
                return redirect('/userAdmin/')
            elif userType == 'S':
                return redirect('/activeRounds/')
            else:
                return redirect('/login/')
        else:
            return redirect('/login/')
    else:
        return redirect('/login/')

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def index(request):
    return login(request)

def fileUpload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

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

def maintainRound(request):
    context = {'roundDetail': RoundDetail.objects.all(),
                'questionnaires': Questionnaire.objects.all()}
    return render(request, 'peer_review/maintainRound.html',context)


def maintainTeam(request):
    context = {'users': User.objects.all(),
                'rounds': RoundDetail.objects.all(),
                'teams': TeamDetail.objects.all()}
    return render(request, 'peer_review/maintainTeam.html', context)


def questionAdmin(request):
    context = {'questionTypes': QuestionType.objects.all(), 'questions': Question.objects.all()}
    return render(request, 'peer_review/questionAdmin.html', context)

def questionnaireAdmin(request):
    context = {'rounds': RoundDetail.objects.all(),
               'questions': Question.objects.all()}
    return render(request, 'peer_review/questionnaireAdmin.html', context)

def questionnaire(request, questionnairePk):
	if request.method == "POST":
		context = {'questionnaire': Questionnaire.objects.all(), 'questions' : Question.objects.all(),
			   'questionTypes' : QuestionType.objects.all(), 'questionOrder' : QuestionOrder.objects.all(),
			   'questionGrouping' : QuestionGrouping.objects.all(), 'questionnairePk' : int(questionnairePk),
               'questionRanking' : Rank.objects.all(), 'questionChoices' : Choice.objects.all()}
		return render(request, 'peer_review/questionnaire.html', context)
	else:
		return render(request, 'peer_review/userError.html')

def userError(request):
	return render(request, 'peer_review/userError.html')

def userList(request):
    users = User.objects.all
    userForm = UserForm()
    docForm = DocumentForm()

    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir)
    file = open(file_path + '/text/email.txt', 'r+')
    emailText = file.read()
    file.close()

    return render(request, 'peer_review/userAdmin.html', {'users': users, 'userForm': userForm, 'docForm': docForm, 'email_text': emailText})

def getTeams(request):
    response={}
    if request.method == "GET":
        teams = TeamDetail.objects.all()
        for team in teams:
            user = User.objects.get(userDetail=team.userDetail)
            response[team.pk] = {
                'userId': user.userId,
                'initials': team.userDetail.initials,
                'surname': team.userDetail.surname,
                'round': team.roundDetail.name,
                'team': team.teamName,
                'status': team.status,
                'teamId': team.pk
            }
    elif request.method == "POST":
        userPk = request.POST.get("pk")
        user = User.objects.get(pk=userPk)
        userDetail = user.userDetail

        teams = TeamDetail.objects.filter(userDetail=userDetail)
        for team in teams:
            response[team.pk] = {
                'round': team.roundDetail.name,
                'team': team.teamName,
                'status': team.status,
                'teamId': team.pk
            }
    return JsonResponse(response)

def getTeamsForRound(request, roundPk):
    teams = TeamDetail.objects.filter(roundDetail_id=roundPk)
    response = {}
    for team in teams:
        response[team.pk] = {
            'userId': team.userDetail.pk,
            'teamName': team.teamName,
            'status': team.status
        }
    # print(response)
    return JsonResponse(response)

def changeUserTeamForRound(request, roundPk, userPk, teamName):
    try:
        team = TeamDetail.objects.filter(userDetail_id=userPk).get(roundDetail_id=roundPk)
    except TeamDetail.DoesNotExist:
        team = TeamDetail(
            userDetail = UserDetail.objects.get(pk=userPk),
            roundDetail = RoundDetail.objects.get(pk=roundPk)
        )
    team.teamName = teamName
    if teamName == 'emptyTeam':
        team.status = 'NA'
    team.save()
    return JsonResponse({'success': True})

def changeTeamStatus(request, teamPk, status):
    team = TeamDetail.objects.get(pk=teamPk)
    team.status = status
    team.save()
    return JsonResponse({'success': True})

def generate_OTP():
    N = random.randint(4, 10)
    OTP = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
                  for _ in range(N))
    return OTP

def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

def generate_email(OTP, post_name, post_surname, email_text, email):
    fn = "{firstname}"
    ln = "{lastname}"
    otp = "{otp}"
    datetime = "{datetime}"
    login = "{login}"

    email_subject = "Pinocchio Confirm Registration"

    email_text = email_text.replace(fn, post_name)
    email_text = email_text.replace(ln, post_surname)
    email_text = email_text.replace(otp, OTP)
    email_text = email_text.replace(datetime, time.strftime("%H:%M:%S %d/%m/%Y"))
    email_text = email_text.replace(login, email)

    print(email_text)

    #send_mail(email_subject, email_text, 'no-reply@pinocchio.up.ac.za', [email], fail_silently=False)

def submitForm(request):
    if request.method == "POST":
        userForm = UserForm(request.POST)
        if userForm.is_valid():
            post_title = userForm.cleaned_data['title']
            post_initials = userForm.cleaned_data['initials']
            post_name = userForm.cleaned_data['name']
            post_surname = userForm.cleaned_data['surname']
            post_cell = userForm.cleaned_data['cell']
            post_email = userForm.cleaned_data['email']

            userDetail = UserDetail(title=post_title, initials=post_initials, name=post_name, surname=post_surname,
                                    cell=post_cell, email=post_email)
            userDetail.save()

            post_userId = userForm.cleaned_data['userId']

            OTP = generate_OTP()

            module_dir = os.path.dirname(__file__)
            file_path = os.path.join(module_dir)
            file = open(file_path + '/text/email.txt', 'a+')
            file.seek(0)
            emailText = file.read()
            file.close()

            generate_email(OTP, post_name, post_surname, emailText, post_email)
            post_password = hash_password(OTP)

            post_status = userForm.cleaned_data['status']

            user = User(userId=post_userId, password=post_password, status=post_status, userDetail=userDetail)
            user.save()

            for roundObj in RoundDetail.objects.all():
                team = TeamDetail(userDetail=userDetail, roundDetail=roundObj)
                team.save()

            return HttpResponseRedirect("../")
    else:
        userForm = UserForm()
    return HttpResponseRedirect("../")

def userProfile(request, userPk):
    if request.method == "GET":
        user = User.objects.get(pk=userPk)
        userDetail = user.userDetail

    return render(request, 'peer_review/userProfile.html', {'user': user, 'userDetail': userDetail})


def userDelete(request):
    if request.method == "POST":
        toDelete = request.POST.getlist("toDelete[]")

        for userPk in toDelete:
            user = User.objects.get(pk=userPk)
            userDetail = user.userDetail

            userDetail.delete()
            user.delete()

    return HttpResponseRedirect('../')

def userUpdate(request, userPk):
    if request.method == "POST":
        user = User.objects.get(pk=userPk)
        userDetail = user.userDetail

        post_userId = request.POST.get("userId")
        post_title = request.POST.get("title")
        post_initials = request.POST.get("initials")
        post_name = request.POST.get("name")
        post_surname = request.POST.get("surname")
        post_cell = request.POST.get("cell")
        post_email = request.POST.get("email")
        post_status = request.POST.get("status")

        user.userId = post_userId
        user.status = post_status
        userDetail.title = post_title
        userDetail.initials = post_initials
        userDetail.name = post_name
        userDetail.surname = post_surname
        userDetail.cell = post_cell
        userDetail.email = post_email

        user.save()
        userDetail.save()
    return HttpResponseRedirect('../')

def resetPassword(request, userPk):
    if request.method == "POST":
        user = User.objects.get(pk=userPk)
        userDetail = user.userDetail

        OTP = generate_OTP()
        generate_email(OTP, userDetail.name, userDetail.surname)
        password = hash_password(OTP)

        user.password = password
        user.save()
        userDetail.save()

        print(OTP)
        print(password)
        print(check_password(password, OTP))
        return HttpResponseRedirect('../')

def addCSVInfo(userList):
    for row in userList:
        OTP = generate_OTP()
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir)
        file = open(file_path + '/text/email.txt', 'a+')
        file.seek(0)
        emailText = file.read()
        file.close()

        generate_email(OTP, row['name'], row['surname'], emailText, row['email'])
        password = hash_password(OTP)

        userDetail = UserDetail(title=row['title'], initials=row['initials'], name=row['name'], surname=row['surname'],
                                cell=row['cell'], email=row['email'])
        userDetail.save()

        user = User(userId=row['user_id'], password=password, status=row['status'], userDetail=userDetail)
        user.save()
    return #todo return render request

def submitCSV(request):
    global errortype
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            filePath = newdoc.docfile.url
            filePath = filePath[1:]

            userList = list()
            error = False

            documents = Document.objects.all()

            count = 0
            with open(filePath) as csvfile:
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

                        userList.append(row)
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

                        if os.path.isfile(filePath):
                            os.remove(filePath)

                        return render(request, 'peer_review/csvError.html',
                                      {'message': message, 'row': rowlist, 'error': errortype})
        else:
            form = DocumentForm()
            message = "Oops! Something seems to be wrong with the CSV file."
            errortype = "No file selected."
            return render(request, 'peer_review/csvError.html', {'message': message, 'error': errortype})

        if not(error):
            addCSVInfo(userList)

    if os.path.isfile(filePath):
        os.remove(filePath)
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

def updateEmail(request):
    if request.method == "POST":
        emailText = request.POST.get("emailText")

        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir)
        file = open(file_path + '/text/email.txt', 'w+')

        file.write(emailText)
        file.close()
    return HttpResponseRedirect('../')

def addTeamCSVInfo(teamList):
    for row in teamList:
        userDetID = User.objects.get(userId=row['userID']).userDetail_id
        roundDetID = RoundDetail.objects.get(name=row['roundDetail']).pk
        changeUserTeamForRound("", roundDetID, userDetID, row['teamName'])
    return 1

def submitTeamCSV(request):
    global errortype
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            filePath = newdoc.docfile.url
            filePath = filePath[1:]

            teamList = list()
            error = False

            documents = Document.objects.all()

            count = 0
            with open(filePath) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    count += 1
                    valid = validateTeamCSV(row)
                    if valid == 0:
                        print(row['userID'])
                        teamList.append(row)
                    else:
                        error = True
                        message = "Oops! Something seems to be wrong with the CSV file at row " + str(count) + "."

                        rowlist = list()
                        rowlist.append(row['userID'])
                        rowlist.append(row['roundDetail'])
                        rowlist.append(row['teamName'])

                        if valid == 1:
                            errortype = "Incorrect number of fields."
                        elif valid == 2:
                            errortype = "Not all fields contain values."
                        elif valid == 3:
                            errortype = "User ID is not a number."
                        elif valid == 4:
                            errortype = "User ID or Round Name does not exist"
                            
                        os.remove(filePath)
                        return render(request, 'peer_review/csvError.html',
                                      {'message': message, 'row': rowlist, 'error': errortype})
        else:
            form = DocumentForm()
            message = "Oops! Something seems to be wrong with the CSV file."
            errortype = "No file selected."
            os.remove(filePath)
            return render(request, 'peer_review/csvError.html', {'message': message, 'error': errortype})

        if not(error):
            addTeamCSVInfo(teamList)
    os.remove(filePath)
    return HttpResponseRedirect('../')


def validateTeamCSV(row):
    # 0 = correct
    # 1 = incorrect number of fields
    # 2 = missing value/s
    # 3 = incorrect format
    # 4 = user/round does not exist

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
            try:
                user = User.objects.get(pk=value).userDetail_id
                #roundD = 
            except User.DoesNotExist:
                return 4
            
    return 0

def getTypeID(questionType):
    # -1 = Error
    # 1 = Choice
    # 2 = Rank
    # 3 = Label
    # 4 = Rate
    # 5 = Freeform

    if questionType == "Choice":
        return 1
    elif questionType == "Rank":
        return 2
    elif questionType == "Label":
        return 3
    elif questionType == "Rate":
        return 4
    elif questionType == "Freeform":
        return 5
    else:
        return -1


def getGroupID(questionGroup):
    # -1 = Error
    # 1 = None
    # 2 = Rest
    # 3 = All

    if questionGroup == "None":
        return 1
    elif questionGroup == "Rest":
        return 2
    elif questionGroup == "All":
        return 3
    else:
        return -1

#Get the list of questions (Label, Publish Date, Type, Grouping)
def getQuestionList(request):
    questions = Question.objects.all()
    labels = []
    publishDates = []
    types = []
    groupings = []
    ids = []

    for question in questions:
        labels.append(question.questionLabel)
        publishDates.append(question.pubDate)
        types.append(str(question.questionType))
        groupings.append(str(question.questionGrouping))
        ids.append(question.pk)

    return JsonResponse({'labels': labels,
                         'publishDates': publishDates,
                         'types': types,
                         'groupings': groupings,
                         'ids': ids})

#Get a question and it's details
def getQuestion(request, qPk):
    question = Question.objects.get(pk=qPk)
    qGrouping = question.questionGrouping.grouping
    labels = []
    if qGrouping == 'Label':
        qLabels = Label.objects.filter(question=question)
        index = 0
        for label in qLabels:
            labels.append(label.labelText)
            index += 1

    response = {'questionText': question.questionText, 
                'questionType': question.questionType.name,
                'questionGrouping': qGrouping,
                'questionLabel': question.questionLabel,
                'labels': labels,
                }

    return JsonResponse(response)

#Get the Choice objects associated with a Choice question
def getChoices(request, qPk):
    question = Question.objects.get(pk=qPk)
    choices = Choice.objects.filter(question=question)
    response = {};
    for choice in choices:
        response[choice.num] = choice.choiceText
    return JsonResponse(response)

#Get the Rank object associated with a Rank question
def getRank(request, qPk):
    q = Question.objects.get(pk=qPk)
    rank = Rank.objects.get(question = q)
    return JsonResponse({'firstWord': rank.firstWord, 'secondWord': rank.secondWord})

#Gets the Rate objects associated with a Rate question
def getRates(request, qPk):
    q = Question.objects.get(pk=qPk)
    rate = Rate.objects.get(question=q)

    return JsonResponse({'topWord': rate.topWord, 
                        'bottomWord': rate.bottomWord,
                        'optional' : rate.optional})

#Gets the Freeform objects associated with a Rate question
def getFreeformItems(request, qPk):
    q = Question.objects.get(pk=qPk)
    freeformItem = FreeformItem.objects.get(question=q)

    return JsonResponse({'freeformType': freeformItem.freeformType})

#Delete a question
def questionDelete(request, qPk):
    if request.method == "POST":
        question = Question.objects.get(pk=qPk)
        question.delete()
        return HttpResponse('Success! Question was deleted successfully.')
    else:
        return HttpResponse('Error.')

#Create a question
def createQuestion(request):
    if request.method == "POST":
        qText = request.POST['question']
        qType = QuestionType.objects.get(name=request.POST['questionType'])
        qGrouping = QuestionGrouping.objects.get(grouping=request.POST['grouping'])
        qLabel = request.POST['questionLabel']
        qPubDate = timezone.now()
        print("Saving new question: Type = '%s', Label = '%s', Grouping = '%s'" % (qType, qLabel, qGrouping))

        if 'pk' in request.POST:
            print('Deleting old question')
            q = Question.objects.get(pk = request.POST['pk'])
            qPubDate = q.pubDate
            q.delete()

        #Save the question
        print('Creating question')
        q = Question(questionText = qText,
                     #pubDate = timezone.now() - datetime.timedelta(days=1),
                     pubDate = qPubDate,
                     questionType = qType,
                     questionGrouping = qGrouping,
                     questionLabel=qLabel
                     )
        q.save()


        if str(qGrouping) == 'Label':
            qLabels = request.POST.getlist('labelArr[]')
            print("Grouping is label: %s" % qLabels)

            for label in qLabels:
                l = Label(question = q, labelText = label)
                l.save()

        #Choice
        if str(qType) == 'Choice':
            choices = request.POST.getlist('choices[]')
            print("Choices = %s" % choices)
           
            #Save the choices
            rank = 0
            for choice in choices:
                c = Choice(question = q,
                           choiceText = choice,
                           num = rank)
                rank += 1
                # print(c)
                c.save()

        #Rank
        elif str(qType) == 'Rank':
            wordOne = request.POST["firstWord"]
            wordTwo = request.POST["secondWord"]
            print("First Word: '%s', Second Word: '%s'" % (wordOne, wordTwo))

            #Save the rank
            r = Rank(question=q,
                     firstWord=wordOne,
                     secondWord=wordTwo)
            r.save()

        #Freeform
        elif str(qType) == 'Freeform':
            FreeformItem.objects.create(question = q, freeformType = request.POST['freeformType'])

        #Rate
        elif str(qType) == 'Rate':
            if request.POST['optional'] == "false":
                optional = False
            else:
                optional = True

            Rate.objects.create(question = q,
                                topWord = request.POST['topWord'],
                                bottomWord = request.POST['bottomWord'],
                                optional = optional)
    return HttpResponse()

def saveQuestionnaire(request):
    if request.method == 'POST':
        intro = request.POST.get("intro")
        label = request.POST.get("label")
        print(label)

        if 'pk' in request.POST:
            q = Questionnaire.objects.get(pk = request.POST.get('pk'))
            q.intro = intro
            q.label = label
            QuestionOrder.objects.filter(questionnaire = q).delete()
            q.save()
        else:
            q = Questionnaire.objects.create(intro = intro, label = label)

        index = 0
        questionOrders = request.POST.getlist('questionOrders[]')
        for question in questionOrders:
            qO = QuestionOrder.objects.create(questionnaire = q,
                               question = Question.objects.get(pk = question),
                               order = index)
            index += 1

    return  HttpResponse('Success')

def deleteQuestionnaire(request, qPk):
    if request.method == "POST":
        q = Questionnaire.objects.get(pk = qPk)
        q.delete()
    return HttpResponse()

def getQuestionnaireList(request):
    questionnaires = Questionnaire.objects.all();
    json = {'labels': [], 'ids': []}
    for q in questionnaires:
        json['labels'].append(q.label)
        json['ids'].append(q.pk)
    return JsonResponse(json)

def getQuestionnaire(request, qPk):
    questionnaire = Questionnaire.objects.get(pk = qPk)
    questions = QuestionOrder.objects.filter(questionnaire = questionnaire)
    questionLabels = []
    questionPubDates = []
    questionTypes = []
    questionGroupings = []
    questionIds = []
    for q in questions:
        questionLabels.append(q.question.questionLabel)
        questionGroupings.append(q.question.questionGrouping.grouping)
        questionTypes.append(q.question.questionType.name)
        questionPubDates.append(q.question.pubDate)
        questionIds.append(q.question.pk)

    json = {'label': questionnaire.label, 
            'intro': questionnaire.intro, 
            'questionLabels': questionLabels, 
            'questionPubDates': questionPubDates, 
            'questionTypes': questionTypes,
            'questionGroupings': questionGroupings,
            'questionIds': questionIds}
    return JsonResponse(json)

def roundDelete(request, roundPk):
    round = RoundDetail.objects.get(pk = roundPk)
    round.delete()
    return HttpResponseRedirect('../')

def roundUpdate(request, roundPk):
    #print('Editing')
    if request.method == "POST":
        round = RoundDetail.objects.get(pk=roundPk)

        post_startingDate =request.POST.get("startingDate")





        post_description = request.POST.get("desc")
        post_questionnaire = request.POST.get("questionn")
        #print(post_questionnaire)

       # for obj in Test.objects.all():
    #obj.start_datetime = time.strptime(obj.start_time, "%d %b %y")
    #obj.save()

#datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")

        
        #post_startingDate = post_startingDate
        post_name = request.POST.get("name")
        #to_datetime("startingDate", format="%y-%m-%d %H:%M")
        #"2016-11-06 16:30"
        #post_startingDate.substr(0, post_startingDate.length - 1);
        # post_startingDate = datetime.datetime.strptime("startingDate", "%d/%m/%y %H:%M")
       # w=getFullYear(post_startingDate)
        #print(w)



        post_endingDate = request.POST.get("endingDate")

        round.description = post_description
        round.questionnaire = Questionnaire.objects.get(pk=post_questionnaire)
        round.name = post_name
        #if post_startingDate !='':
        round.startingDate = post_startingDate
            #string[0: len(post_startingDate) - 1];
            

        #if post_endingDate !='':
        round.endingDate = post_endingDate

        round.save()
    return HttpResponseRedirect('../')
    #return HttpResponse()

#Create a round
def createRound(request):
    #print('Creating Round')
    if 'description' in request.GET:
        rDescription = request.GET['description']

        try:
            rQuestionnaire = Questionnaire.objects.get(pk=request.GET['questionnaire'])
        except Questionnaire.DoesNotExist:
            rQuestionnaire = None

   # rQuestionnaire =Questionnaire.objects.get(intro=request.GET['questionnaire'])
        rStartingDate = request.GET['startingDate']
        rEndingDate = request.GET['endingDate']
        rName = request.GET['name']
       # rIsEditing = request.GET['isEditing']
       # qPubDate = timezone.now()
      #  print("Saving new question"): Description = '%s', Questionnaire = '%s'" % (rDescription, rQuestionnaire))"

        #if qIsEditing == 'true':
         #   print('Deleting old question')
         #   q = Question.objects.get(questionLabel = qLabel)
          #  qPubDate = q.pubDate
          #  q.delete()

        #Save the question
        print('Creating Round')
        r = RoundDetail(description = rDescription,
                     #pubDate = timezone.now() - datetime.timedelta(days=1),
                     questionnaire = rQuestionnaire,
                     startingDate = rStartingDate,
                     name = rName,
                     endingDate = rEndingDate,
                     )
        r.save()
    #
    #return HttpResponseRedirect('../maintainRound')
    return HttpResponse()



