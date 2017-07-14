import csv
import os
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

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
    team = get_object_or_404(TeamDetail, pk=team_pk)
    team.status = status
    team.save()
    return JsonResponse({'success': True})


@admin_required
def change_user_team_for_round(request, round_pk, user_id, team_name):
    try:
        team = TeamDetail.objects.filter(user_id=user_id).get(roundDetail_id=round_pk)
    except TeamDetail.DoesNotExist:
        team = TeamDetail(
            user=get_object_or_404(User, user_id=user_id),
            roundDetail=get_object_or_404(RoundDetail, pk=round_pk)
        )

    team.teamName = team_name
    if team_name == 'emptyTeam':
        team.delete()
    else:
        team.save()
    return JsonResponse({'success': True})


@admin_required
def get_teams_for_round(request, round_pk):
    teams = TeamDetail.objects.filter(roundDetail_id=round_pk)
    response = {}
    team_sizes = {}

    for team in teams:
        if team.teamName not in team_sizes:
            team_sizes[team.teamName] = 0
        team_sizes[team.teamName] += 1

    for team in teams:
        response[team.pk] = {
            'user_id': team.user.user_id,
            'teamName': team.teamName,
            'status': team.status,
            'teamSize': team_sizes[team.teamName]
        }
    # print(response)
    return JsonResponse(response)


@admin_required
def get_teams(request):
    response = {}
    if request.method == "GET":
        teams = TeamDetail.objects.all()
        for team in teams:
            try:
                user = User.objects.get(pk=team.user.pk)
            except User.DoesNotExist:
                return JsonResponse("Team has a user which doesn't exist")
            response[team.pk] = {
                'user_id': user.user_id,
                'initials': team.user.initials,
                'surname': team.user.surname,
                'round': team.roundDetail.name,
                'team': team.teamName,
                'status': team.status,
                'teamId': team.pk,
            }
    elif request.method == "POST":
        user_pk = request.POST.get("pk")
        user = get_object_or_404(User, pk=user_pk)

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
    try:
        for row in team_list:
            user_det_id = User.objects.get(user_id=row['user_id']).pk
            round_det_id = RoundDetail.objects.get(name=row['roundDetail']).pk
            change_user_team_for_round("", round_det_id, user_det_id, row['teamName'])
        return 1
    except User.DoesNotExist:
        return "One of the Users does not exist"
    except RoundDetail.DoesNotExist:
        return "One of the Rounds does not exist"


@admin_required
def submit_team_csv(request):
    if not request.user.is_authenticated():
        return user_error(request)

    global error_type
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            new_doc = Document(doc_file=request.FILES['doc_file'])
            new_doc.save()

            file_path = new_doc.doc_file.url
            file_path = file_path[1:]

            team_list = list()
            error = False

            count = 0
            with open(file_path) as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    count += 1
                    valid = validate_team_csv(row)
                    if valid == 0:
                        print(row['user_id'])
                        team_list.append(row)
                    else:
                        message = "Oops! Something seems to be wrong with the CSV file at row " + str(count) + "."

                        row_list = list()
                        row_list.append(row['user_id'])
                        row_list.append(row['roundDetail'])
                        row_list.append(row['teamName'])

                        if valid == 1:
                            error_type = "Incorrect number of fields."
                        elif valid == 2:
                            error_type = "Not all fields contain values."
                        elif valid == 3:
                            error_type = "user ID is not a number."

                        os.remove(file_path)
                        return render(request, 'peer_review/csvError.html',
                                      {'message': message, 'row': row_list, 'error': error_type})
        else:
            message = "Oops! Something seems to be wrong with the CSV file."
            error_type = "No file selected."
            return render(request, 'peer_review/csvError.html', {'message': message, 'error': error_type})

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
        if key == "user_id":
            try:
                int(value)
            except ValueError:
                return 3
    return 0
