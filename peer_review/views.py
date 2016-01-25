from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from django.http import JsonResponse
import random
import string
import hashlib
import uuid

import datetime
import csv
import os

from django.utils import timezone

from .models import Document
from .models import Question, QuestionType, QuestionGrouping, Choice, Rank, Questionnaire, RoundDetail, TeamDetail, FreeformItem, Rate, Label
from .models import User, UserDetail
from .models import Questionnaire, QuestionOrder
from .forms import DocumentForm, UserForm

def studentHomePage(request):
    context = {}
    return render(request, 'peer_review/studentHomePage.html',context)

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def index(request):
    users = User.objects.all
    userForm = UserForm()
    docForm = DocumentForm()
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir)
    file = open(file_path + '/text/email.txt', 'a+')
    file.seek(0)
    emailText = file.read()
    file.close()

    return render(request, 'peer_review/userAdmin.html', {'users': users, 'userForm': userForm, 'docForm': docForm, 'email_text': emailText})


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
			   'questionGrouping' : QuestionGrouping.objects.all(), 'questionnairePk' : int(questionnairePk)}
		return render(request, 'peer_review/questionnaire.html', context)
	else:
		return render(request, 'peer_review/userError.html')

def userError(request):
	return render(request, 'peer_review/userError.html')

def userList(request):
    users = User.objects.all
    userForm = UserForm()
    docForm = DocumentForm()
    return render(request, 'peer_review/userAdmin.html', {'users': users, 'userForm': userForm, 'docForm': docForm})

def getTeams(request):
    teams = TeamDetail.objects.all()
    response={}
    for team in teams:
        user = User.objects.get(userDetail=team.userDetail)
        response[team.pk] = {
            'userId': user.userId,
            'initials': team.userDetail.initials,
            'surname': team.userDetail.surname,
            'round': team.roundDetail.description,
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

def generate_email(OTP, post_name, post_surname):
    email = "Welcome to Pinocchio " + post_name + " " + post_surname + "\n\nYour one time password is: " + OTP + \
        "\n\nKind regards,\nThe Pinocchio Team"
    # ToDo implement email notification

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
            generate_email(OTP, post_name, post_surname)
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

def userDelete(request, userPk):
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
        generate_email(OTP, row['name'], row['surname'])
        password = hash_password(OTP)

        userDetail = UserDetail(title=row['title'], initials=row['initials'], name=row['name'], surname=row['surname'],
                                cell=row['cell'], email=row['email'])
        userDetail.save()

        user = User(userId=row['user_id'], password=password, status=row['status'], userDetail=userDetail)
        user.save()

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

            # ToDo delete older files

            count = 0
            with open(filePath) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    count += 1
                    if validate(row) == 1:
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
                        if validate(row) == 0:
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

                        if validate(row) == 2:
                            errortype = "Not all fields contain values."
                        if validate(row) == 3:
                            errortype = "Cell or user ID is not a number."
                        if validate(row) == 4:
                            errortype = "User already exists."

                        return render(request, 'peer_review/csvError.html',
                                      {'message': message, 'row': rowlist, 'error': errortype})
        else:
            form = DocumentForm()
            message = "Oops! Something seems to be wrong with the CSV file."
            errortype = "No file selected."
            return render(request, 'peer_review/csvError.html', {'message': message, 'error': errortype})

        if not(error):
            addCSVInfo(userList)
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
        file = open(file_path + '/text/email.txt', 'w')

        file.write(emailText)
        file.close()
        
def addTeamCSVInfo(teamList):
    for row in teamList:
        userDetID = User.objects.get(userId=row['userID']).userDetail_id
        changeUserTeamForRound("", row['roundDetail'], userDetID, row['teamName'])
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
                            errortype = "user ID is not a number."

                        return render(request, 'peer_review/csvError.html',
                                      {'message': message, 'row': rowlist, 'error': errortype})
        else:
            form = DocumentForm()
            message = "Oops! Something seems to be wrong with the CSV file."
            errortype = "No file selected."
            return render(request, 'peer_review/csvError.html', {'message': message, 'error': errortype})

        if not(error):
            addTeamCSVInfo(teamList)
    return HttpResponseRedirect('../')


def validateTeamCSV(row):
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

    for question in questions:
        labels.append(question.questionLabel)
        publishDates.append(question.pubDate)
        types.append(str(question.questionType))
        groupings.append(str(question.questionGrouping))

    return JsonResponse({'labels': labels,
                         'publishDates': publishDates,
                         'types': types,
                         'groupings': groupings})

#Get a question and it's details
def getQuestion(request):
    questionLabel = request.GET['questionLabel']
    question = Question.objects.get(questionLabel=questionLabel)
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
def getChoices(request):
    questionLabel = request.GET['questionLabel']
    question = Question.objects.get(questionLabel=questionLabel)
    choices = Choice.objects.filter(question=question)
    response = {};
    for choice in choices:
        response[choice.num] = choice.choiceText
    return JsonResponse(response)

#Get the Rank object associated with a Rank question
def getRank(request):
    questionLabel = request.GET['qL']
    q = Question.objects.get(questionLabel=questionLabel)
    rank = Rank.objects.get(question = q)
    return JsonResponse({'firstWord': rank.firstWord, 'secondWord': rank.secondWord})

#Gets the Rate objects associated with a Rate question
def getRates(request):
    #Probably going to have to change this
    questionLabel = request.GET['qL']
    q = Question.objects.get(questionLabel=questionLabel)
    rates = Rate.objects.filter(question=q)

    optionalArr = []
    scaleArr = []
    #There aren't even text fields in the model
    #choices = []

    for r in rates:
        optionalArr.append(r.optional)
        scaleArr.append(r.numberOfOptions)

    return JsonResponse({'optionalArr': optionalArr, 'scaleArr': scaleArr})

#Gets the Freeform objects associated with a Rate question
def getFreeformItems(request):
    questionLabel = request.GET['qL']
    q = Question.objects.get(questionLabel=questionLabel)
    freeformItems = FreeformItem.objects.filter(question=q)
    print(freeformItems)

    typeArr = []
    valueArr = []

    for f in freeformItems:
        typeArr.append(f.freeformType)
        valueArr.append(f.value)

    return JsonResponse({'typeArr': typeArr, 'valueArr': valueArr})

#Delete a question
def questionDelete(request):
    if request.method == "POST":
        questionLabel = request.POST['questionLabel']
        question = Question.objects.get(questionLabel=questionLabel)
        question.delete()
        return HttpResponse('Success! Question was deleted successfully.')
    else:
        return HttpResponse('Error.')

#Create a question
def createQuestion(request):
    if 'question' in request.GET:
        qText = request.GET['question']
        qType = QuestionType.objects.get(name=request.GET['questionType'])
        qGrouping = QuestionGrouping.objects.get(grouping=request.GET['grouping'])
        qLabel = request.GET['questionLabel']
        qIsEditing = request.GET['isEditing']
        qPubDate = timezone.now()
        print("Saving new question: Type = '%s', Label = '%s', Grouping = '%s'" % (qType, qLabel, qGrouping))

        if qIsEditing == 'true':
            print('Deleting old question')
            q = Question.objects.get(questionLabel = qLabel)
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
            qLabels = request.GET.getlist('labelArr[]')
            print("Grouping is label: %s" % qLabels)

            for label in qLabels:
                l = Label(question = q, labelText = label)
                l.save()

        #Choice
        if str(qType) == 'Choice':
            choices = request.GET.getlist('choices[]')
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
            wordOne = request.GET["firstWord"]
            wordTwo = request.GET["secondWord"]
            print("First Word: '%s', Second Word: '%s'" % (wordOne, wordTwo))

            #Save the rank
            r = Rank(question=q,
                     firstWord=wordOne,
                     secondWord=wordTwo)
            r.save()

        #Freeform
        elif str(qType) == 'Freeform':
            types = request.GET.getlist('types[]')
            values = request.GET.getlist('values[]')
            print(types)
            print("Types: %s, Values:" % types, values)

            rank = 0
            for t in types:
                f = FreeformItem(question = q,
                                 value = values[rank],
                                 freeformType = t
                                 )
                rank += 1
                f.save()

        #Rate
        elif str(qType) == 'Rate':
            optionalArr = request.GET.getlist('optionalArr[]')
            scaleArr = request.GET.getlist('scaleArr[]')
            choiceArr = request.GET.getlist('choiceArr[]')

            index = 0
            for r in choiceArr:
                print('Optional: %s' % optionalArr[index])
                r = Rate(question = q,
                         numberOfOptions = scaleArr[index],
                         optional = (optionalArr[index] == "true"),
                         num = index)
                r.save()
                index += 1

    else:
        message = 'You submitted an empty form.'
    return HttpResponse()

def roundDelete(request, roundPk):
    round = RoundDetail.objects.get(pk = roundPk)
    round.delete()
    return HttpResponseRedirect('../')

def roundUpdate(request, roundPk):
    if request.method == "POST":
        round = RoundDetail.objects.get(pk=roundPk)

        post_description = request.POST.get("description")
        post_questionnaire = request.POST.get("questionnaire")
        post_startingDate = request.POST.get("startingDate")
        post_endingDate = request.POST.get("endingDate")

        round.description = post_description
        round.questionnaire = post_questionnaire
        round.startingDate = post_startingDate
        round.endingDate = post_endingDate

        round.save()
    return HttpResponseRedirect('../')
