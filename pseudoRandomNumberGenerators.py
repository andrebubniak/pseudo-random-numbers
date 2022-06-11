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
    