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
from .forms import DocumentForm, StudentForm, StudentDetailForm

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
    students = Student.objects.all
    if request.method == "POST":
        studentForm = StudentForm(request.post)
        studentDetailForm = StudentDetailForm(request.post)
        if studentForm.is_valid() and studentDetailForm.is_valid():
            student = studentForm.save(commit = False)
            StudentDetail = studentDetailForm.save(commit = False)

            student.author = request.user
            studentDetail.author = request.user

            student.save()
            studentDetail.save()
            return HttpResponseRedirect('.')
    else:
        studentForm = StudentForm()
        studentDetailForm = StudentDetailForm()
    return render(request, 'peer_review/user_list.html',{'students': students, 'studentForm': studentForm, 'studentDetailForm': studentDetailForm})

    # users = Student.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
    # if request.method == "POST":
    #     form = UserForm(request.POST)
    #     if form.is_valid():
    #         user = form.save(commit = False)
    #         user.author = request.user
    #         user.created_date = timezone.now()
    #         user.save()
    #         return HttpResponseRedirect('.')
    # else:
    #     form = UserForm()
    # return render(request, 'user/user_list.html', {'users': users, 'form': form})

def user_delete(request, user_id):
    u = User.objects.get(pk = user_id).delete()
    return HttpResponseRedirect('../')