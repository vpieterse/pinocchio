import random


def generate_otp():
    n = random.randint(4, 10)
    otp = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
                  for _ in range(n))
    return otp
