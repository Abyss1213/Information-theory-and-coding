import sys

def C3encode(d: str):
    D = '0'+'0'+d[0]+'0'+d[1:4]+'0'+d[4:]
    b = 0
    for i in range(15):
        if D[i] == '1':
            b ^= i+1
    p = bin(b)[2:].zfill(4)[::-1]
    r = p[0] + p[1] + d[0] + p[2] + d[1:4] + p[3] + d[4:]
    return r


def intertwine(R: list):
    # m = len(R) % 3
    # for i in range(3-m):
    #     R.append('0'*15)
    L = len(R)
    res = []
    for i in range(0, L, 3):
        a, b, c = R[i], R[i+1], R[i+2]
        A, B, C = '', '', ''
        for j in range(0, 15, 3):
            A += a[j]+b[j+1]+c[j+2]
            B += b[j]+c[j+1]+a[j+2]
            C += c[j]+a[j+1]+b[j+2]
        res.append(A)
        res.append(B)
        res.append(C)
    return res


def Encode():
    d = input()
    l = len(d)
    R = []
    for i in range(0, l, 11):
        r = C3encode(d[i:11+i])
        R.append(r)
    res = intertwine(R)
    for x in res:
        sys.stdout.write(x)

Encode()



