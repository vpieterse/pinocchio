from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from peer_review.decorators.adminRequired import admin_required

from ..models import Question, Questionnaire, RoundDetail, QuestionOrder, User, TeamDetail


# Render the questionnaireAdmin template
# @admin_required
def questionnaire_admin(request):
    context = {'questions': Question.objects.all(),
               'questionnaires': get_questionnaires()}
    return render(request, 'peer_review/questionnaireAdmin.html', context)

@admin_required
def questionnaire_preview(request, questionnaire_pk):
    alice = User(title='Miss', initials='A', name='Alice', surname='Test', userId='Alice')
    bob = User(title='Mr', initials='B', name='Bob', surname='Test', userId='Bob')
    carol = User(title='Miss', initials='C', name='Carol', surname='Test', userId='Carol')
    
    questionnaire = Questionnaire.objects.get(pk=questionnaire_pk)
    q_orders = QuestionOrder.objects.filter(questionnaire=questionnaire)
    
    mockRound = RoundDetail(name='Preview Round', questionnaire=questionnaire, description='This is a preview round')
    
    team_name = 'Preview'
    teamDetailAlice = TeamDetail(user=alice, roundDetail=mockRound, teamName=team_name)
    teamDetailBob = TeamDetail(user=bob, roundDetail=mockRound, teamName=team_name)
    teamDetailCarol = TeamDetail(user=carol, roundDetail=mockRound, teamName=team_name)
    
    q_team = [alice, bob, carol]
    context = {'questionOrders': q_orders, 'teamMembers': q_team, 'questionnaire': questionnaire, 'currentUser': alice, 'round': 0, 'preview': 1}
    return render(request, 'peer_review/questionnaire.html', context)

# Save a questionnaire
@admin_required
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
@admin_required
def edit_questionnaire(request, questionnaire_pk):
    context = {'questions': Question.objects.all(),
               'questionnaires': get_questionnaires,
               'questionnaire': Questionnaire.objects.get(pk=questionnaire_pk),
               'questionOrders': QuestionOrder.objects.filter(
                   questionnaire=Questionnaire.objects.get(pk=questionnaire_pk))}
    return render(request, 'peer_review/questionnaireAdmin.html', context)


# Delete a questionnaire
@admin_required
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
# @admin_required
def get_questionnaires():
    response = []
    for questionnaire in Questionnaire.objects.all():
        response.append({'title': questionnaire.label,
                         'intro': questionnaire.intro,
                         'pk': questionnaire.pk,
                         'inARound': RoundDetail.objects.filter(questionnaire=questionnaire).exists()
                         })
    return response
