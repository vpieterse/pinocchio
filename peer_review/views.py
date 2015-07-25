from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from django.utils import timezone

import datetime

from .models import Document
from .models import Question, QuestionType
from .models import User, UserDetail
from .forms import DocumentForm, UserForm

def createQuestion(request):
    if 'question' in request.GET:
        text = request.GET['question']
        message = 'Inserting Question with text: %r' % text
        qType = QuestionType.objects.get(name='Rank')
        q = Question(questionText=text,
                     pubDate=timezone.now() - datetime.timedelta(days=1),
                     questionType=qType,
                     questionGrouping=3        
                     )
        q.save()
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
    return render(request, 'peer_review/userAdmin.html', {'users': users, 'userForm': userForm})

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

            message = "Success"
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
    user = User.objects.get(pk = userPk)