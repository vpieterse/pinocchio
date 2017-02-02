from django.contrib import messages
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from peer_review.forms import ResetForm
from peer_review.generate_otp import generate_otp
from peer_review.models import RoundDetail, TeamDetail, User
from peer_review.views import generate_otp_email, hash_password


def account_details(request):
    if not request.user.is_authenticated():
        return user_error(request)
    user = User.objects.get(userId=request.user.userId)
    context = {'user': user}
    return render(request, 'peer_review/accountDetails.html', context)


def active_rounds(request):
    if not request.user.is_authenticated():
        return user_error(request)
    user = request.user
    teams = TeamDetail.objects.filter(user=user).order_by('roundDetail__startingDate')
    #exp_teams = TeamDetail.objects.filter(user=user and roundDetail.endingDate<datetime.date.now())
    context = {'teams': teams}
    return render(request, 'peer_review/activeRounds.html', context)


def get_team_members(request):
    if not request.user.is_authenticated():
        return user_error(request)

    user = request.user
    rounds = RoundDetail.objects.all()
    team_list = []
    team_members = []
    for team in TeamDetail.objects.filter(user=user):
        teamName = team.teamName
        roundName = RoundDetail.objects.get(pk=team.roundDetail.pk).name
        team_list.append(team)
        for teamItem in TeamDetail.objects.filter(teamName=team.teamName):
            if teamItem.user != user:
                print(teamItem)
                team_members.append(teamItem)
    context = {'teams': team_list, 'members': team_members}
    print(team_list)
    print(team_members)
    return render(request, 'peer_review/teamMembers.html', context)


def reset_password(request, userId):
    if request.method == "POST":
        userPk = userId
        user = User.objects.get(userId=userPk)

        new_otp = generate_otp()
        generate_otp_email(new_otp, user.name, user.surname, user.email)
        password = hash_password(new_otp)

        user.password = password
        user.save()

        return HttpResponseRedirect('../')


def user_error(request):
    # Renders error page with a 403 status code for forbidden users
    return HttpResponseForbidden(render(request, 'peer_review/userError.html'))


def user_reset_password(request):
    if request.method == 'POST':
        form = ResetForm(request.POST)
        if form.is_valid():
            userId = form.cleaned_data['userId']
            user = User.objects.get(userId=userId)
            if user:
                # Reset OTP for user
                # messages.add_message(request, messages.success, "Password reset")
                return reset_password(request, user.userId)
            else:
                # Email not found
                messages.add_message(request, messages.ERROR, "Could not find a user " + userId)
                return redirect('/forgotPassword/')
    else:
        return redirect('/login/')
