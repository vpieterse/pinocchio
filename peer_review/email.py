import os
import time
import logging

from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

def generate_otp_email(user_otp, post_name, post_surname, email, user_id):
    fn = "{first_name}"
    ln = "{last_name}"
    otp = "{otp}"
    datetime = "{datetime}"
    login = "{login}"
    post_user_id = "{user_id}"

    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir)
    file = open(file_path + '/text/otp_email.txt', 'a+')
    file.seek(0)
    email_text = file.read()
    file.close()

    email_subject = "Pinocchio Confirm Registration"

    email_text = email_text.replace(fn, post_name)
    email_text = email_text.replace(ln, post_surname)
    email_text = email_text.replace(otp, user_otp)
    email_text = email_text.replace(datetime, time.strftime("%H:%M:%S %d/%m/%Y"))
    email_text = email_text.replace(login, email)
    email_text = email_text.replace(post_user_id, user_id)

    print(email_text)

    if settings.EMAIL_HOST != "":
        send_mail(email_subject, email_text, settings.FROM_EMAIL_ADDRESS, [email], fail_silently=False)
    else:
        logger.warning("No EMAIL_HOST configured; Did not attempt to send email.")