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


def Encode():
    d = input()
    l = len(d)
    for i in range(0, l, 11):
        r = C3encode(d[i:11+i])
        sys.stdout.write(r)

Encode()



