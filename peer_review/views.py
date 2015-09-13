from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from django.utils import timezone

import datetime
import csv

from .models import Document
from .models import Question, QuestionType, QuestionGrouping, Choice, Header, Rank
from .models import User, UserDetail
from .forms import DocumentForm, UserForm, CSVForm

def createQuestion(request):
    if 'question' in request.GET:
        text = request.GET['question']
        message = 'Inserting Question with text: %r' % text
        qType = QuestionType.objects.get(name=request.GET['questionType'])
        print('qType: %r' % str(qType)) #Check
        if str(qType) == 'Choice':
            qGrouping = QuestionGrouping.objects.get(grouping=request.GET['grouping'])
            choices = request.GET.getlist('choices[]')

            q = Question(questionText=text,
                         pubDate=timezone.now() - datetime.timedelta(days=1),
                         questionType=qType,
                         questionGrouping=qGrouping      
                        )  

            q.save()

            #Temporary header creation
            headers = Header.objects.filter(text=text);
            if len(headers) > 0:
                h = headers[0];
            else:
                h = Header(text=text)
                h.save()

            rank = 0
            for choice in choices:
                c = Choice(header = h,
                           question = q,
                           choiceText = choice,
                           num = rank)
                rank = rank + 1
                print('saving %r' % choice) #Check
                print('as rank %r' % rank)  #Check
                c.save()
        elif str(qType) == 'Rank':
            qGrouping = QuestionGrouping.objects.get(grouping=request.GET['grouping'])
            firstWord = request.GET["firstWord"];
            secondWord = request.GET["secondWord"];


            q = Question(questionText=text,
                         pubDate=timezone.now() - datetime.timedelta(days=1),
                         questionType=qType,
                         questionGrouping=qGrouping      
                        )

            q.save();

            #Temporary header creation
            headers = Header.objects.filter(text=firstWord);
            if len(headers) > 0:
                w1 = headers[0];
            else:
                w1 = Header(text=firstWord)
                w1.save()

            #Temporary header creation
            headers = Header.objects.filter(text=secondWord);
            if len(headers) > 0:
                w2 = headers[0];
            else:
                w2 = Header(text=secondWord)
                w2.save()
                
            r = Rank(question = q,
                    firstWord = w1,
                    secondWord = w2)

            r.save()
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def index(request):
    latest_question_list = Question.objects.order_by('-pubDate')[:5]
    output = ', '.join([p.questionText for p in latest_question_list])
    return HttpResponse(output)

def fileUpload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect('')
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'peer_review/fileUpload.html',
        {'documents': documents, 'form': form}
        ,context_instance=RequestContext(request)
    )

def questionAdmin(request):
    context = {'questionTypes': QuestionType.objects.all()}
    return render(request, 'peer_review/questionAdmin.html', context)

def userList(request):
    users = User.objects.all
    userForm = UserForm()
    csvForm = CSVForm()
    return render(request, 'peer_review/userAdmin.html', {'users': users, 'userForm': userForm, 'csvForm': csvForm})

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

            userDetail = UserDetail(title = post_title, initials = post_initials, name = post_name, surname = post_surname, cell = post_cell, email = post_email)
            userDetail.save()

            post_userId = userForm.cleaned_data['userId']
            post_password = userForm.cleaned_data['password']
            post_status = userForm.cleaned_data['status']

            user = User(userId = post_userId, password = post_password, status = post_status, userDetail = userDetail)
            user.save()

            return HttpResponseRedirect("../")
    else:
        userForm = UserForm()
    return HttpResponseRedirect("../")

def userDelete(request, userPk):
    user = User.objects.get(pk = userPk)
    userDetail = user.userDetail

    userDetail.delete()
    user.delete()
    return HttpResponseRedirect('../')

def userUpdate(request, userPk):
    if request.method == "POST":
        user = User.objects.get(pk = userPk)
        userDetail = user.userDetail

        post_userId = request.POST.get("userId")
        post_title = request.POST.get("title")
        post_initials = request.POST.get("initials")
        post_name = request.POST.get("name")
        post_surname = request.POST.get("surname")
        post_cell = request.POST.get("cell")
        post_email = request.POST.get("email")

        user.userId = post_userId
        userDetail.title = post_title
        userDetail.initials = post_initials
        userDetail.name = post_name
        userDetail.surname = post_surname
        userDetail.cell = post_cell
        userDetail.email = post_email

        user.save()
        userDetail.save()
    return HttpResponseRedirect('../')

def submitCSV(request):
    if request.method == 'POST':
        csvForm = CSVForm(request.POST, request.FILES)
        if csvForm.is_valid():
            return HttpResponse('xxx')
    return HttpResponse('hello2S')
