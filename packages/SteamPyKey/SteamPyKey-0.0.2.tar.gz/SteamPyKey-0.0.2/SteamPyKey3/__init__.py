import random
import string

def MakeKey():
    k1 = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    k2 = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    k3 = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

    return (f'{k1}-{k2}-{k3}')