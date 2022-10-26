import string
import time
import random

def random_string():
    letters = string.ascii_uppercase + string.digits
    random_string = ''.join(random.choices(letters, k=5))
    random_string += str(int(time.time()) % 1000)
    return random_string
