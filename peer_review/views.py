from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext

from .models import Document
from .models import Question
from .forms import DocumentForm

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