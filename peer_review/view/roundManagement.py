import csv
import mimetypes
import time

import os
from wsgiref.util import FileWrapper

from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from peer_review.decorators.adminRequired import admin_required

from peer_review.models import RoundDetail, Questionnaire, Response
from peer_review.view.userFunctions import user_error


@admin_required
def maintain_round(request):
    context = {'roundDetail': RoundDetail.objects.all(),
               'questionnaires': Questionnaire.objects.all()}
    return render(request, 'peer_review/maintainRound.html', context)


def write_dump(round_pk):

    current_round = RoundDetail.objects.get(id=round_pk)
    dump_file = 'media/dumps/' + time.strftime("%Y-%m-%d %H:%M:%S") + 'round_' + str(current_round.name) + '.csv'
    data = [['ResponseID', 'Respondent', 'QuestionTitle', 'LabelTitle', 'SubjectUser', 'Answer']]

    # First, find the row id of the most recent answer to each question
    distinct_responses = Response.objects.filter(roundDetail=round_pk).values(
        "question_id", "user_id", "label_id", "subjectUser_id").annotate(max_id=Max('id'))

    # Filter response id's
    distinct_response_ids = [x['max_id'] for x in distinct_responses]

    # Fetch the most recent responses separately
    round_data = Response.objects.filter(id__in=distinct_response_ids).order_by(
        "user_id", "question_id", "label_id", "subjectUser_id")
    distinct_round_data = round_data.values('user_id', 'question_id', 'label_id', 'subjectUser_id', 'id')

    if len(distinct_round_data) > 0:
        for item_id in distinct_round_data:
            item = round_data.get(id=item_id['id'])
            response_id = item.id
            user_id = item.user.user_id
            question_label = item.question.questionLabel
            label = item.label

            subject_id = ""
            if item.subjectUser:
                subject_id = item.subjectUser.user_id

            if item.answer:
                answer = "<br />".join(item.answer.split("\n"))
            else:
                answer = ""

            data.append([response_id, user_id, question_label, label, subject_id, answer])
    else:
        data.append(['NO DATA'])

    os.makedirs(os.path.dirname(dump_file), exist_ok=True)
    with open(dump_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_ALL)
        writer.writerows(data)

    csv_file.close()
    return str(dump_file)  # Returns dump filename


@admin_required
def round_delete(request):
    if request.method == "POST":
        current_round = get_object_or_404(RoundDetail, pk=request.POST.get("pk"))
        current_round.delete()
    return HttpResponseRedirect('../')


@admin_required
def round_update(request, round_pk):
    try:
        if request.method == "POST":
            current_round = get_object_or_404(RoundDetail, pk=round_pk)

            post_starting_date = request.POST.get("startingDate")
            post_description = request.POST.get("description")
            post_questionnaire = request.POST.get("questionnaire")
            post_name = request.POST.get("roundName")
            post_ending_date = request.POST.get("endingDate")
            current_round.description = post_description
            current_round.questionnaire = Questionnaire.objects.get(pk=post_questionnaire)
            current_round.name = post_name
            current_round.startingDate = post_starting_date
            current_round.endingDate = post_ending_date
            current_round.save()
        return HttpResponseRedirect('../')
    except Questionnaire.DoesNotExist:
        return HttpResponseRedirect('../1')


# Create a round
@admin_required
def create_round(request):
    try:

        if 'description' in request.GET:
            round_description = request.GET['description']
            try:
                round_questionnaire = Questionnaire.objects.get(pk=request.GET['questionnaire'])
            except Questionnaire.DoesNotExist:
                round_questionnaire = None
            round_starting_date = request.GET['startingDate']
            round_ending_date = request.GET['endingDate']
            round_name = request.GET['name']
            current_round = RoundDetail(description=round_description,
                                        questionnaire=round_questionnaire,
                                        startingDate=round_starting_date,
                                        name=round_name,
                                        endingDate=round_ending_date,
                                        )
            current_round.save()
        return HttpResponseRedirect('../maintainRound')
    except ValueError:
        return HttpResponseRedirect('../maintainRound/1')


@admin_required
def maintain_round_with_error(request, error):
    if error == '1':  # Incorrect Date format
        str_error = "Incorrect Date Format yyyy-mm-dd hh"
    else:
        str_error = "Unknown Error"

    context = {'roundDetail': RoundDetail.objects.all(),
               'questionnaires': Questionnaire.objects.all(),
               'error': str_error}
    return render(request, 'peer_review/maintainRound.html', context)


@admin_required
def round_dump(request):
    if request.method == "POST":
        round_pk = request.POST.get("roundPk")
        dump_file = write_dump(round_pk)
        # Download Dump
        wrapper = FileWrapper(open(dump_file))
        content_type = mimetypes.guess_type(dump_file)[0]
        response = HttpResponse(wrapper, content_type=content_type)
        current_round = get_object_or_404(RoundDetail, id=round_pk)
        # response['Content-Length'] = os.path.getsize(dump_file)
        response['Content-Disposition'] = "attachment; filename=" + time.strftime("%Y-%m-%d %H.%M.%S") \
                                          + ' round_' + current_round.name + ".csv"
        return response
    return user_error(request)
