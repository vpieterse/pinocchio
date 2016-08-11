from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from ..models import User, RoundDetail, TeamDetail

def maintain_team(request):
    if request.method == "POST":
        round_pk = request.POST.get("roundPk")

        context = {'users': User.objects.all(),
                   'rounds': RoundDetail.objects.all(),
                   'teams': TeamDetail.objects.all(),
                   'roundPk': round_pk}

    else:
        context = {'users': User.objects.all(),
                   'rounds': RoundDetail.objects.all(),
                   'teams': TeamDetail.objects.all(),
                   'roundPk': "none"}
    return render(request, 'peer_review/maintainTeam.html', context)

def change_team_status(request, team_pk, status):
    team = TeamDetail.objects.get(pk=team_pk)
    team.status = status
    team.save()
    return JsonResponse({'success': True})
	
def change_user_team_for_round(request, round_pk, user_pk, team_name):
    try:
        team = TeamDetail.objects.filter(user_id=user_pk).get(roundDetail_id=round_pk)
    except TeamDetail.DoesNotExist:
        team = TeamDetail(
            user=User.objects.get(pk=user_pk),
            roundDetail=RoundDetail.objects.get(pk=round_pk)
        )
    team.teamName = team_name
    if team_name == 'emptyTeam':
        team.status = 'NA'
    team.save()
    return JsonResponse({'success': True})

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