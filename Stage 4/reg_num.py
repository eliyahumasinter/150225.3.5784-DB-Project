import random
import string
from fleet import FLEET


chosen = []

def generate_registration_num():
    return f'N-{str(random.randint(0,999)).zfill(3)}{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}'


def random_registration_num():
    rn = ""
    
    if len(FLEET) > 0:
        rn = random.choice(FLEET)
        FLEET.remove(rn)
        chosen.append(rn)
    else: 
        rn = generate_registration_num()
        while rn in chosen:
            rn = generate_registration_num()

    return rn

print(random_registration_num())