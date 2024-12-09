from random import randint


# genera stringa corrispondente a id casuale
def create_random_id():
    return str(randint(10000, 99999))
