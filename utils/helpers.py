import random
import string


def generate_random_string():
    # Credit: https://stackoverflow.com/a/2257449
    str_length = 8
    return ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=str_length))