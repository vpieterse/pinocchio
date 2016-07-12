from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from ..models import Question, Questionnaire, RoundDetail, QuestionOrder


# Render the questionnaireAdmin template
@login_required
def questionnaire_admin(request):
    context = {'questions': Question.objects.all(),
               'questionnaires': get_questionnaires()}
    return render(request, 'peer_review/questionnaireAdmin.html', context)


# Save a questionnaire
def save_questionnaire(request):
    if request.method == 'POST':
        intro = request.POST.get("intro")
        title = request.POST.get("title")
        questions = str(request.POST.get('questions')).split(";#")
        if 'pk' in request.POST:
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
def edit_questionnaire(request, questionnaire_pk):
    context = {'questions': Question.objects.all(),
               'questionnaires': get_questionnaires,
               'questionnaire': Questionnaire.objects.get(pk=questionnaire_pk),
               'questionOrders': QuestionOrder.objects.filter(
                   questionnaire=Questionnaire.objects.get(pk=questionnaire_pk))}
    return render(request, 'peer_review/questionnaireAdmin.html', context)


# Delete a questionnaire
def delete_questionnaire(request):
    if request.method == "POST":
        pks = request.POST['pk'].split(';#')
        for pk in pks:
            if str(pk).isdigit():
                Questionnaire.objects.get(pk=pk).delete()
            else:
                messages.add_message(request, messages.WARNING,
                                     "Error: Something went wrong when deleting the questionnaire")
                return HttpResponseRedirect('/questionnaireAdmin')
        messages.add_message(request, messages.SUCCESS, str(len(pks)) + " questionnaire(s) deleted successfully")
        return HttpResponseRedirect('/questionnaireAdmin')
    else:
        return HttpResponseRedirect('/questionnaireAdmin')


# Return a dict with all the questionnaires, including whether each one is contained in a round
def get_questionnaires():
    response = []
    for questionnaire in Questionnaire.objects.all():
        response.append({'title': questionnaire.label,
                         'intro': questionnaire.intro,
                         'pk': questionnaire.pk,
                         'inARound': RoundDetail.objects.filter(questionnaire=questionnaire).exists()
                         })
    return response
