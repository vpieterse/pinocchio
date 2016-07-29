from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

from ..models import Question, Questionnaire, RoundDetail, QuestionOrder, User, TeamDetail, Response, Label

def questionnaire(request, round_pk):
    if not request.user.is_authenticated():
        return user_error(request)
    # user = request.user
    user = get_object_or_404(User, userId = '14785236')  # FOR TEST
    questionnaire = get_object_or_404(RoundDetail, pk=round_pk).questionnaire
    q_orders = QuestionOrder.objects.filter(questionnaire=questionnaire)

    team_name = TeamDetail.objects.get(user=user, roundDetail=RoundDetail.objects.get(pk=round_pk)).teamName
    q_team = User.objects.filter(teamdetail__teamName = team_name, teamdetail__roundDetail = RoundDetail.objects.get(pk=round_pk))

    context = {'questionOrders': q_orders, 'teamMembers': q_team, 'questionnaire': questionnaire, 'currentUser': user,
               'round': round_pk}
    print(context)
    return render(request, 'peer_review/questionnaire.html', context)

def save_questionnaire_progress(request):
    if request.method == "POST":
        question = get_object_or_404(Question, pk=request.POST.get('questionPk'))
        round_detail = get_object_or_404(RoundDetail, pk=request.POST.get('roundPk'))
        user = request.user
        # user = User.objects.get(userId='14035548')  # TEST

        # If grouping == None, there is no label or subjectUser
        if question.questionGrouping.grouping == "None":
            label = None  # test
            subject_user = None  # test
        # If grouping == Label, there is a label but no subjectUser
        elif question.questionGrouping.grouping == "Label":
            label = get_object_or_404(Label, pk=request.POST.get('label'))
            subject_user = None  # test
        # If grouping == Rest || All, there is a subjectUser but no label
        else:
            subject_user = get_object_or_404(Label, pk=request.POST.get('subjectUser'))
            label = None

        answer = request.POST.get('answer')
        batchid = request.POST.get('batchid')
        print(user)
        Response.objects.create(question=question,
                                roundDetail=round_detail,
                                user=user,
                                subjectUser=subject_user,
                                label=label,
                                answer=answer,
                                batchid=batchid)
        return JsonResponse({'result': 0})
    else:
        return JsonResponse({'result': 1})


def get_responses(request):
    question = get_object_or_404(Question, pk=request.GET.get('questionPk'))
    round_detail = get_object_or_404(RoundDetail, pk=request.GET.get('roundPk'))
    user = request.user
    # user = User.objects.get(userId='14035548')  # TEST
    responses = Response.objects.filter(user=user, roundDetail=round_detail, question=question).order_by('batchid').reverse()
    batchid = 0
    count = 0
    for r in responses:
        if batchid==0:
            batchid=r.batchid
        elif not (batchid==r.batchid) :
            break
        count += 1
    responses = responses[0:count]
    # Need to find a way to get the latest responses, instead of all of them
    json = {'answers': [], 'labelOrUserIds': [], 'labelOrUserNames': []}
    for r in responses:
        print(r.__dict__)
        json['answers'].append(r.answer)
        if question.questionGrouping.grouping == "Label":
            json['labelOrUserNames'].append(r.label.labelText)
            json['labelOrUserIds'].append(r.label.id)
        elif question.questionGrouping.grouping != "None":
            json['labelOrUserNames'].append(r.subjectUser.name + ' ' + r.subjectUser.surname)
            json['labelOrUserIds'].append(r.subjectUser.userId)
    return JsonResponse(json)