from ..models import Question, Questionnaire, RoundDetail, QuestionOrder
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

#Render the questionnaireAdmin template
@login_required
def questionnaireAdmin(request):
    context = {'questions': Question.objects.all(),
               'questionnaires': getQuestionnaires()}
    return render(request, 'peer_review/questionnaireAdmin.html', context)

#Save a questionnaire
def saveQuestionnaire(request):
    if request.method == 'POST':
        intro = request.POST.get("intro")
        title = request.POST.get("title") 
        questions = str(request.POST.get('questions')).split(";#");
        if ('pk' in request.POST):
            q = Questionnaire.objects.get(pk=request.POST.get("pk"))
            QuestionOrder.objects.filter(questionnaire=q).delete()
            q.intro = intro
            q.label = title
            q.save()
        elif Questionnaire.objects.filter(label=title).exists():
            messages.add_message(request, messages.WARNING, "Error: A question with that title already exists.")
            return HttpResponseRedirect('/questionnaireAdmin')
        else:
            q = Questionnaire.objects.create(intro=intro, label=title)

        for index, question in enumerate(questions):
            if question.isdigit():
                qo = QuestionOrder.objects.create(questionnaire=q,
                                                  question=Question.objects.get(pk=question),
                                                  order=index)
        messages.add_message(request, messages.SUCCESS, "Questionnaire saved successfully.")
    return HttpResponseRedirect('/questionnaireAdmin')
    
# Render the questionnaireAdmin template with the questionnaires details filled in
@login_required
def editQuestionnaire(request, questionnairePk):
    context = {'questions': Question.objects.all(),
               'questionnaires': getQuestionnaires,
               'questionnaire': Questionnaire.objects.get(pk=questionnairePk),
               'questionOrders': QuestionOrder.objects.filter(questionnaire=Questionnaire.objects.get(pk=questionnairePk))}
    return render(request, 'peer_review/questionnaireAdmin.html', context)

# Delete a questionnaire
def deleteQuestionnaire(request):
    if request.method == "POST":
        pks = request.POST['pk'].split(';#')
        for pk in pks:
            if str(pk).isdigit():
                Questionnaire.objects.get(pk=pk).delete()
            else:
                messages.add_message(request, messages.WARNING, "Error: Something went wrong when deleting the questionnaire")
                return HttpResponseRedirect('/questionnaireAdmin')
        messages.add_message(request, messages.SUCCESS, str(len(pks)) + " questionnaire(s) deleted successfully")
        return HttpResponseRedirect('/questionnaireAdmin')
    else:
        return HttpResponseRedirect('/questionnaireAdmin')

# Return a dict with all the questionnaires, including whether each one is contained in a round
def getQuestionnaires():
    response = []
    for questionnaire in Questionnaire.objects.all():
        response.append({'title': questionnaire.label,
                        'intro': questionnaire.intro,
                        'pk': questionnaire.pk,
                        'inARound': RoundDetail.objects.filter(questionnaire=questionnaire).exists()
                        })
    return response