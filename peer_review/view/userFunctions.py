import base64
import os
from time import sleep

from django.contrib import messages
from django.core.signing import Signer, TimestampSigner
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from pip._vendor.requests.packages.urllib3.exceptions import TimeoutStateError

from peer_review.email import generate_otp_email
from peer_review.forms import ResetForm
from peer_review.generate_otp import generate_otp
from peer_review.models import RoundDetail, TeamDetail, User
from pinocchio import settings


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

        user.set_password(new_otp)
        user.save()

        return HttpResponseRedirect('../')


# Sign and urlsafe Base64 encode a user ID with
# a timestamp. Returns result as string
def sign_userId(userId):
    id_signer = TimestampSigner()
    signed = id_signer.sign(userId)

    b64encoded = base64.urlsafe_b64encode(signed.encode('utf-8'))
    return b64encoded.decode('utf-8')


# Unsign a given url-save base64 encoded userId
# to a string. Returns the user id if successful;
# on failure, returns None. This function can fail
# when the encoded userId has expired (max age) or
# the signed key is invalid.
def unsign_userId(b64UserId, maxAge=None):
    try:
        id_signer = TimestampSigner()
        unencoded_user_id = base64.urlsafe_b64decode(b64UserId.encode('utf-8')).decode('utf-8')
        signed = id_signer.unsign(unencoded_user_id, maxAge)
        return signed.split(':', 1)[0]

    except Exception as e:
        print(e)
        return None


# Sends a password-reset email containing a signed
# key as authentication. Returns a boolean;
# True = email sent,
# False = error
def send_password_request_email(userId, email_addr, post_name, post_surname):
   try:
        fn = "{firstname}"
        ln = "{lastname}"
        url = "{url}"

        requestURL = 'http://localhost:8000/recoverPassword/' + sign_userId(userId)

        file_path = settings.BASE_DIR + '/peer_review/text/password_request.txt'
        file = open(file_path, 'a+')
        file.seek(0)
        email_text = file.read()
        file.close()

        email_subject = "Pinocchio Password Reset Request"

        email_text = email_text.replace(fn, post_name)
        email_text = email_text.replace(ln, post_surname)
        email_text = email_text.replace(url, requestURL)

        print(email_text)

        # TODO: REMOVE THIS COMMENT IN THE LIVE VERSION
        # send_mail(email_subject, email_text, 'pinocchio@cs.up.ac.za', [email_addr], fail_silently=False)

        return True

   except Exception as e:
       print(e)
       return False


def user_error(request):
    # Renders error page with a 403 status code for forbidden users
    return HttpResponseForbidden(render(request, 'peer_review/userError.html'))


def user_reset_password(request):
    if request.method == 'POST':
        form = ResetForm(request.POST)
        if form.is_valid():
            userId = form.cleaned_data['userId']

            try:
                user = User.objects.get(userId=userId)
                # Reset OTP for user // NO MORE
                # messages.add_message(request, messages.success, "Password reset")
                success = send_password_request_email(
                    userId=userId,
                    email_addr=user.email,
                    post_name=user.name,
                    post_surname=user.email
                )
                #return reset_password(request, user.userId)
                if success:
                    messages.add_message(request, messages.SUCCESS,
                                         "Sending email to <strong>" + user.email + "</strong>. Please go"
                                                                                    " and check your inbox.")
                return redirect('/forgotPassword/')

            except User.DoesNotExist:
                # Email not found
                messages.add_message(request, messages.ERROR, "Could not find a user " + userId)
                return redirect('/forgotPassword/')
    else:
        return redirect('/login/')
