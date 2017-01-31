import os
import time


def generate_email(user_otp, post_name, post_surname, email):
    fn = "{firstname}"
    ln = "{lastname}"
    otp = "{otp}"
    datetime = "{datetime}"
    login = "{login}"

    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir)
    file = open(file_path + '/text/email.txt', 'a+')
    file.seek(0)
    email_text = file.read()
    file.close()

    email_subject = "Pinocchio Confirm Registration"

    email_text = email_text.replace(fn, post_name)
    email_text = email_text.replace(ln, post_surname)
    email_text = email_text.replace(otp, user_otp)
    email_text = email_text.replace(datetime, time.strftime("%H:%M:%S %d/%m/%Y"))
    email_text = email_text.replace(login, email)

    print(email_text)

    #send_mail(email_subject, email_text, 'no-reply@pinocchio.cs.up.ac.za', [email], fail_silently=False)