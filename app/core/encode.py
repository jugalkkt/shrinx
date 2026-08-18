def encode(n:str):
    a = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    ans = ""
    n = int(n)
    rem = n % 62
    div = n // 62
    ans += a[rem]
    while (div):
        n = div
        rem = n % 62
        div = n // 62
        ans += a[rem]
    ans = ans[::-1]
    return ans