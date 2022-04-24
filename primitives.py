def mult(x, y):
    result = x*y
    if result > 1.0:
        return 1.0
    return result

def add(x, y):
    result = x+y
    if result > 1.0:
        return 1.0
    return result

def sub(x, y):
    result = x-y
    if result < 0.0:
        return 0.0
    return result

def div(x, y):
    if y == 0:
        return 0
    result = x/y
    if result > 1.0:
        return 1.0
    return result