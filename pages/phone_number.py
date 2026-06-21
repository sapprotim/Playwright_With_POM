import random

def generate_fake_sg_phone():
    random_number = random.randint(1000, 9999)
    return "+658345" + str(random_number)