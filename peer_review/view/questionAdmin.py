from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from ..models import Question, QuestionOrder, QuestionType, Choice, Rank, Rate, FreeFormItem, Label
from peer_review.decorators.adminRequired import admin_required


def user_error(request):
    # Renders error page with a 403 status code for forbidden users
    return HttpResponseForbidden(render(request, 'peer_review/userError.html'))


def is_user_staff(request):
    if request.user.is_staff or request.user.is_superuser:
        return True
    else:
        return False


# Render the questionAdmin template
@admin_required
def question_admin(request):
    # print(request.user.is_authenticated())
    # if not request.user.is_authenticated():
    #     return render(request, "peer_review/login.html")
    if not is_user_staff(request):
        return user_error(request)

    context = {'questions': get_questions()}
    return render(request, 'peer_review/questionAdmin.html', context)


# Render the questionAdmin template with the questions detailed loaded in
@admin_required
def edit_question(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    context = {'question': question,
               'questions': get_questions(),
               'choices': Choice.objects.filter(question=question),
               'freeFormType': str(FreeFormItem.objects.filter(question=question).first()),
               'rate': Rate.objects.filter(question=question).first(),
               'rank': Rank.objects.filter(question=question).first()}
    return render(request, 'peer_review/questionAdmin.html', context)


# Delete a question
@admin_required
def delete_question(request):
    if request.method == "POST":
        pks = request.POST['question-pk'].split(';#')
        for pk in pks:
            get_object_or_404(Question, pk=pk).delete()
        messages.add_message(request, messages.SUCCESS, str(len(pks)) + " question(s) deleted successfully")
        return HttpResponseRedirect('/questionAdmin')
    else:
        return HttpResponseRedirect('/questionAdmin')


# Save question
@admin_required
def save_question(request):
    if request.method == "POST":
        question_text = str(request.POST['question-content'])
        question_title = str(request.POST['question-title'])
        question_type = str(request.POST['question-type'])
        if not QuestionType.objects.filter(name=question_type).exists():
            QuestionType.objects.create(name=question_type)

        if 'question-pk' in request.POST:
            q = get_object_or_404(Question, pk=request.POST['question-pk'])
            Choice.objects.filter(question=q).delete()
            Rank.objects.filter(question=q).delete()
            Rate.objects.filter(question=q).delete()
            FreeFormItem.objects.filter(question=q).delete()
            q.questionText = question_text
            q.questionLabel = question_title
            q.pubDate = timezone.now()
            q.save()
        elif Question.objects.filter(questionLabel=question_title).exists():
            messages.add_message(request, messages.WARNING, "Error: A question with that title already exists.")
            return HttpResponseRedirect('/questionAdmin')
        else:
            q = Question.objects.create(questionText=question_text,
                                        pubDate=timezone.now(),
                                        questionType=QuestionType.objects.get(name=question_type),
                                        questionLabel=question_title
                                        )

        if question_type == 'Choice':
            choices = str(request.POST['question-choices']).split(";#")
            for index, choice in enumerate(choices):
                Choice.objects.create(question=q, choiceText=choice, num=index)
        elif question_type == 'Rank':
            Rank.objects.create(question=q,
                                firstWord=str(request.POST["rank-first"]),
                                secondWord=str(request.POST["rank-second"]))
        elif question_type == 'Rate':
            Rate.objects.create(question=q,
                                topWord=request.POST['rate-first'],
                                bottomWord=request.POST['rate-second'],
                                optional=('rate-optional' in request.POST))
        elif question_type == 'FreeForm':
            FreeFormItem.objects.create(question=q, freeFormType=request.POST['freeForm-type'])

    messages.add_message(request, messages.SUCCESS, "Question saved successfully")
    return HttpResponseRedirect('/questionAdmin')


# Return a dict with all the questions, including whether each one is contained in a round
def get_questions():
    response = []
    for question in Question.objects.all():
        response.append({'title': question.questionLabel,
                         'date': question.pubDate,
                         'type': str(question.questionType),
                         'pk': question.pk,
                         'inAQuestionnaire': QuestionOrder.objects.filter(question=question).exists()})
    return response


# Checks if a question with the same title already exists
@admin_required
def check_question(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if Question.objects.filter(questionLabel=title).exists():
            return JsonResponse({'result': 1})
        else:
            return JsonResponse({'result': 0})

