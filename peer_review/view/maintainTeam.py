import csv
import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from ..models import User, RoundDetail, TeamDetail, Document
from peer_review.decorators.adminRequired import admin_required
from peer_review.forms import DocumentForm
from peer_review.view.userFunctions import user_error



@admin_required
def maintain_team(request):
    if request.method == "POST":
        round_pk = request.POST.get("roundPk")

        context = {'users': User.objects.filter(Q(is_active=1) & (Q(status='S') | Q(status='U'))),
                   'rounds': RoundDetail.objects.all(),
                   'teams': TeamDetail.objects.all(),
                   'roundPk': round_pk}

    else:
        context = {'users': User.objects.filter(Q(is_active=1) & (Q(status='S') | Q(status='U'))),
                   'rounds': RoundDetail.objects.all(),
                   'teams': TeamDetail.objects.all(),
                   'roundPk': "none"}
    return render(request, 'peer_review/maintainTeam.html', context)


@admin_required
def change_team_status(request, team_pk, status):
    team = TeamDetail.objects.get(pk=team_pk)
    team.status = status
    team.save()
    return JsonResponse({'success': True})


@admin_required
def change_user_team_for_round(request, round_pk, userId, team_name):
    try:
        team = TeamDetail.objects.filter(user_id=userId).get(roundDetail_id=round_pk)
    except TeamDetail.DoesNotExist:
        team = TeamDetail(
            user=User.objects.get(userId=userId),
            roundDetail=RoundDetail.objects.get(pk=round_pk)
        )
    team.teamName = team_name
    if team_name == 'emptyTeam':
        team.status = 'NA'
    team.save()
    return JsonResponse({'success': True, 'team_pk': team.pk})


@admin_required
def get_teams_for_round(request, round_pk):
    teams = TeamDetail.objects.filter(roundDetail_id=round_pk)
    response = {}
    for team in teams:
        response[team.pk] = {
            'userId': team.user.userId,
            'teamName': team.teamName,
            'status': team.status,
        }
    # print(response)
    return JsonResponse(response)


@admin_required
def get_teams(request):
    response = {}
    if request.method == "GET":
        teams = TeamDetail.objects.all()
        for team in teams:
            user = User.objects.get(pk=team.user.pk)
            response[team.pk] = {
                'userId': user.userId,
                'initials': team.user.initials,
                'surname': team.user.surname,
                'round': team.roundDetail.name,
                'team': team.teamName,
                'status': team.status,
                'teamId': team.pk,
            }
    elif request.method == "POST":
        user_pk = request.POST.get("pk")
        user = User.objects.get(pk=user_pk)

        teams = TeamDetail.objects.filter(user=user)
        for team in teams:
            response[team.pk] = {
                'round': team.roundDetail.name,
                'team': team.teamName,
                'status': team.status,
                'teamId': team.pk,
                'roundPk': team.roundDetail.pk
            }
    return JsonResponse(response)


@admin_required
def add_team_csv_info(team_list):
    for row in team_list:
        user_det_id = User.objects.get(userId=row['userID']).pk
        round_det_id = RoundDetail.objects.get(name=row['roundDetail']).pk
        change_user_team_for_round("", round_det_id, user_det_id, row['teamName'])
    return 1


@admin_required
def submit_team_csv(request):
    if not request.user.is_authenticated():
        return user_error(request)

    global errortype
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            file_path = newdoc.docfile.url
            file_path = file_path[1:]

            team_list = list()
            error = False

            documents = Document.objects.all()

            count = 0
            with open(file_path) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    count += 1
                    valid = validate_team_csv(row)
                    if valid == 0:
                        print(row['userID'])
                        team_list.append(row)
                    else:
                        error = True
                        message = "Oops! Something seems to be wrong with the CSV file at row " + str(count) + "."

                        row_list = list()
                        row_list.append(row['userID'])
                        row_list.append(row['roundDetail'])
                        row_list.append(row['teamName'])

                        if valid == 1:
                            errortype = "Incorrect number of fields."
                        elif valid == 2:
                            errortype = "Not all fields contain values."
                        elif valid == 3:
                            errortype = "user ID is not a number."

                        os.remove(file_path)
                        return render(request, 'peer_review/csvError.html',
                                      {'message': message, 'row': row_list, 'error': errortype})
        else:
            form = DocumentForm()
            message = "Oops! Something seems to be wrong with the CSV file."
            errortype = "No file selected."
            return render(request, 'peer_review/csvError.html', {'message': message, 'error': errortype})

        if not error:
            add_team_csv_info(team_list)
    return HttpResponseRedirect('../')


def validate_team_csv(row):
    # 0 = correct
    # 1 = incorrect number of fields
    # 2 = missing value/s
    # 3 = incorrect format

    if len(row) != 3:
        return 1
    for key, value in row.items():
        if value is None:
            return 2
        if key == "userID":
            try:
                int(value)
            except ValueError:
                return 3
    return 0
