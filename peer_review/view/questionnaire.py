from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from peer_review.decorators.userRequired import user_required

from ..models import Question, RoundDetail, QuestionOrder, User, TeamDetail, Response, Label


@user_required
def questionnaire(request, round_pk):
    user = request.user
    try:
        round_object = RoundDetail.objects.get(pk=round_pk)
        questionnaire_object = round_object.questionnaire

        q_orders = QuestionOrder.objects.filter(questionnaire=questionnaire_object)
        team_name = TeamDetail.objects.get(user=user, roundDetail=RoundDetail.objects.get(pk=round_pk)).teamName
        q_team = User.objects.filter(teamdetail__teamName=team_name,
                                     teamdetail__roundDetail=RoundDetail.objects.get(pk=round_pk))

        # Does the user have access to this page?
        # Has the questionnaire expired / is it in the future?
        if round_object.startingDate > timezone.now():
            messages.add_message(request, messages.ERROR, "That questionnaire is not yet available.")
            return redirect('activeRounds')

        if round_object.endingDate < timezone.now():
            messages.add_message(request, messages.ERROR, "That questionnaire has expired.")
            return redirect('activeRounds')

        context = {'questionOrders': q_orders, 'teamMembers': q_team, 'questionnaire': questionnaire_object,
                   'currentUser': user,
                   'round': round_pk}
        return render(request, 'peer_review/questionnaire.html', context)

    except (RoundDetail.DoesNotExist, QuestionOrder.DoesNotExist, TeamDetail.DoesNotExist, User.DoesNotExist):
        messages.add_message(request, messages.ERROR, "The questionnaire is currently unavailable.")
        return redirect('activeRounds')


# Returning a JsonResponse with a result field of 1 indicates an error in saving the questionnaire progress
# A 0 indicates success
@user_required
def save_questionnaire_progress(request):
    if request.method == "POST":
        try:
            question = Question.objects.get(pk=request.POST.get('questionPk'))
            round_detail = RoundDetail.objects.get(pk=request.POST.get('roundPk'))
            team_detail = TeamDetail.objects.get(user=User.objects.get(user_id=request.user.user_id),
                                                 roundDetail=request.POST.get('roundPk'))
            team_detail.status = TeamDetail.IN_PROGRESS
            team_detail.save()
        except (Question.DoesNotExist, RoundDetail.DoesNotExist, TeamDetail.DoesNotExist):
            return JsonResponse({'result': 1})
        user = request.user
        # user = User.objects.get(userId='14035548')  # TEST

        # If grouping == None, there is no label or subjectUser
        if question.questionGrouping.grouping == "None":
            label = None 
            subject_user = None
        # If grouping == Label, there is a label but no subjectUser
        elif question.questionGrouping.grouping == "Label":
            try:
                label = Label.objects.get(pk=request.POST.get('label'))
                subject_user = None
            except Label.DoesNotExist:
                return JsonResponse({'result': 1})
        # If grouping == Rest || All, there is a subjectUser but no label
        else:
            try:
                subject_user = User.objects.get(pk=request.POST.get('subjectUser'))
                label = None
            except User.DoesNotExist:
                return JsonResponse({'result': 1})
        answer = request.POST.get('answer')
        batch_id = request.POST.get('batch_id')
        Response.objects.create(question=question,
                                roundDetail=round_detail,
                                user=user,
                                subjectUser=subject_user,
                                label=label,
                                answer=answer,
                                batch_id=batch_id)
        return JsonResponse({'result': 0})
    else:
        return JsonResponse({'result': 1})


@user_required
def get_responses(request):
    question = get_object_or_404(Question, pk=request.GET.get('questionPk'))
    round_detail = get_object_or_404(RoundDetail, pk=request.GET.get('roundPk'))
    user = request.user

    responses = Response.objects.filter(user=user,
                                        roundDetail=round_detail,
                                        question=question).order_by('batch_id').reverse()
    batch_id = 0
    count = 0

    for r in responses:
        if batch_id == 0:
            batch_id = r.batch_id
        elif not (batch_id == r.batch_id):
            break
        count += 1
    responses = responses[0:count]
    print(responses)
    json = {'answers': [], 'labelOrUserIds': [], 'labelOrUserNames': []}
    for r in responses:
        json['answers'].append(r.answer)
        if question.questionGrouping.grouping == "Label":
            json['labelOrUserNames'].append(r.label.labelText)
            json['labelOrUserIds'].append(r.label.id)
        elif question.questionGrouping.grouping != "None":
            json['labelOrUserNames'].append(r.subjectUser.name + ' ' + r.subjectUser.surname)
            json['labelOrUserIds'].append(r.subjectUser.user_id)
    return JsonResponse(json)