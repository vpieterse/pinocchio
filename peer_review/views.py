from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext

from .models import Document
from .models import Question
from .models import Student
from .models import StudentDetail
from .forms import DocumentForm, UserForm

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
    return render(request, 'peer_review/questionAdmin.html')

def student_list(request):
    studentDetail = StudentDetail.objects.all
    userForm = UserForm()
    return render(request, 'peer_review/userAdmin.html', {'studentDetail': studentDetail, 'userForm': userForm})

def get_studentFormData(request):
    if request.method == "POST":
        userForm = UserForm(request.POST)
        if userForm.is_valid():
            post_username = userForm.cleaned_data['username']
            post_password = userForm.cleaned_data['password']
            post_status = userForm.cleaned_data['status']

            student = Student(username = post_username, password = post_password, status = post_status)
            student.save()

            post_title = userForm.cleaned_data['title']
            post_initials = userForm.cleaned_data['initials']
            post_name = userForm.cleaned_data['name']
            post_surname = userForm.cleaned_data['surname']
            post_cell = userForm.cleaned_data['cell']
            post_email = userForm.cleaned_data['email']

            studentDetail = StudentDetail(student = student, title = post_title, initials = post_initials, name = post_name, surname = post_surname, cell = post_cell, email = post_email)
            studentDetail.save()
            return HttpResponseRedirect('./userAdmin')
    else:
        userForm = UserForm()
    return render(request, 'peer_review/userAdmin.html')

def user_delete(request, user_id):
    studentDetail = StudentDetail.objects.get(student__username = user_id)
    student = studentDetail.student

    studentDetail.delete()
    student.delete()
    return HttpResponseRedirect('../userAdmin')