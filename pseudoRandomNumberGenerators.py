import time
from typing import List


def glim3_generator(quantity: int, seed: int = None) -> List[float]:
    if(quantity < 1): return
    if(seed == None or seed <= 0): seed = round(time.time())

    a = 8404997
    c = 1
    m = pow(2, 35)
    
    numbers = []
    numbers.append(seed)
    numbers.append(((seed * a + c) % m) / m)

    for i in range(1, quantity):
        numbers.append(((numbers[i] * m * a + c) % m) / m)

    return numbers[1:]
    

def generator_multiplicative_congruential(quantity: int, seed: int = None, t: int = None, p: int=None) -> List[float]:
    if(quantity < 1): return
    if(seed == None or seed <= 0): seed = round(time.time())

    if p==None:
        p = 31  
    if t==None:
        t = 2727  
    m = pow(2, p) - 1
    a =  8*t-3
    
    numbers = []
    numbers.append(seed)
    numbers.append(((seed * a) % m) / m)

    for i in range(1, quantity):
        numbers.append(((numbers[i] * m * a) % m) / m)

    return numbers[1:]