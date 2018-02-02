import base64
import logging
from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from peer_review.decorators.userRequired import user_required
from peer_review.forms import ResetForm
from peer_review.models import RoundDetail, TeamDetail, User
from pinocchio import baseSettings

logger = logging.getLogger(__name__)

@user_required
def account_details(request):
    user = get_object_or_404(User, user_id=request.user.user_id)
    reset_link = '/recoverPassword/' + sign_user_id(request.user.user_id)

    context = {'user': user, 'reset_link': reset_link, 'is_logged_user': True}
    return render(request, 'peer_review/accountDetails.html', context)


@user_required
def member_details(request, user_id):
    if not request.user.is_authenticated():
        return user_error(request)
    member = get_object_or_404(User, user_id=user_id)
    context = {'user': member, 'is_logged_user': False}
    return render(request, 'peer_review/accountDetails.html', context)


@user_required
def active_rounds(request):
    user = request.user
    teams = TeamDetail.objects.filter(user=user).order_by('roundDetail__startingDate')
    rounds = RoundDetail.objects.all()
    # exp_teams = TeamDetail.objects.filter(user=user and roundDetail.endingDate<datetime.date.now())
    context = {'teams': teams, 'rounds': rounds}
    return render(request, 'peer_review/activeRounds.html', context)


@user_required
def get_team_members(request):
    if not request.user.is_authenticated():
        return user_error(request)

    user = request.user
    team_list = []

    # Create a list of teams
    # Each team object contains the team object itself and a list of teammates
    for team in TeamDetail.objects.filter(user=user):
        member_list = []
        for teamMember in TeamDetail.objects.filter(teamName=team.teamName):
            if teamMember.user != user:
                member_list.append(teamMember)

        team_list.append({
            'team': team,
            'members': member_list
        })

    context = {'teams': team_list}
    return render(request, 'peer_review/teamMembers.html', context)


# Sign and urlsafe Base64 encode a user ID with
# a timestamp. Returns result as string
def sign_user_id(user_id):
    id_signer = TimestampSigner()
    signed = id_signer.sign(user_id)

    b64encoded = base64.urlsafe_b64encode(signed.encode('utf-8'))
    return b64encoded.decode('utf-8')


# Unsign a given url-save base64 encoded userId
# to a string. Returns the user id if successful;
# on failure, returns None. This function can fail
# when the encoded userId has expired (max age) or
# the signed key is invalid.
def unsign_user_id(b64_user_id, max_age=None):
    try:
        id_signer = TimestampSigner()
        unencoded_user_id = base64.urlsafe_b64decode(b64_user_id.encode('utf-8')).decode('utf-8')
        signed = id_signer.unsign(unencoded_user_id, max_age)
        return signed.split(':', 1)[0]

    except Exception as e:
        print(e)
        return None


# Sends a password-reset email containing a signed
# key as authentication. Returns a boolean;
# True = email sent,
# False = error
def send_password_request_email(user_id, email_address, post_name, post_surname):
    try:
        fn = "{first_name}"
        ln = "{last_name}"
        url = "{url}"

        request_url = settings.EXTERNAL_URL + 'recoverPassword/' + sign_user_id(user_id)

        file_path = baseSettings.BASE_DIR + '/peer_review/text/password_request.txt'
        file = open(file_path, 'a+')
        file.seek(0)
        email_text = file.read()
        file.close()

        email_subject = "Pinocchio Password Reset Request"

        email_text = email_text.replace(fn, post_name)
        email_text = email_text.replace(ln, post_surname)
        email_text = email_text.replace(url, request_url)

        print(email_text)

        # Emails are sent here
        if settings.EMAIL_HOST != "":
            send_mail(email_subject, email_text, settings.EMAIL_HOST, [email_address], fail_silently=False)
        else:
            logger.warning("No EMAIL_HOST configured; Did not attempt to send email.")

        return True
    except SMTPException as e:
        logger.error('Error while sending mail: ' + e)
        raise e

def user_error(request):
    # Renders error page with a 403 status code for forbidden users
    return HttpResponseForbidden(render(request, 'peer_review/userError.html'))


def user_reset_password(request):
    if request.method == 'POST':
        form = ResetForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']

            try:
                user = User.objects.get(user_id=user_id)
                # Reset OTP for user // NO MORE
                # messages.add_message(request, messages.success, "Password reset")
                try:
                    success = send_password_request_email(
                        user_id=user_id,
                        email_address=user.email,
                        post_name=user.name,
                        post_surname=user.surname
                    )
                    # return reset_password(request, user.userId)
                    if success:
                        messages.add_message(request, messages.SUCCESS,
                                             "Sending email to <strong>" + user.email + "</strong>. Please go"
                                                                                        " and check your inbox.")
                except Exception as e:
                    messages.add_message(request, messages.ERROR, "There was an error while sending the reset email. "
                                                                  "Contact admin if the problem persists.")

                return redirect('/forgotPassword/')

            except User.DoesNotExist:
                # Email not found
                messages.add_message(request, messages.ERROR, "Could not find a user " + user_id)
                return redirect('/forgotPassword/')
    else:
        return redirect('/login/')
