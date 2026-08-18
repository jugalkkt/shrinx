def index(i: str):
    a = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    for j in range(62):
        if (a[j] == i): 
            return j
    return 0
def decode(n: str):
    acc = 0
    for i in n:
        acc = acc*62 + int(index(i))
    return acc