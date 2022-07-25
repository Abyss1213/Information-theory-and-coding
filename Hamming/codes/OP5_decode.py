import sys


def recover(r: str): # 假设编码时分组正好是3的倍数
    R = []
    for i in range(0, len(r), 15):
        R.append(r[i:i+15])
    res = []
    for i in range(0, len(R), 3):
        A, B, C = R[i], R[i+1], R[i+2]
        a, b, c = '', '', ''
        for j in range(0, 15, 3):
            a += A[j]+C[j+1]+B[j+2]
            b += B[j]+A[j+1]+C[j+2]
            c += C[j]+B[j+1]+A[j+2]
        res.append(a)
        res.append(b)
        res.append(c)
    return res


def C3decode(r: str):
    b = 0
    for i in range(15):
        if r[i] == '1':
            b ^= i+1
    if b != 0:
        if r[b-1] == '0':
            r = r[0:b-1] + '1' + r[b:]
        else:
            r = r[0:b-1] + '0' + r[b:]
    d = r[2]+r[4:7]+r[8:]
    return d


def Decode():
    r = input()
    R = recover(r)
    for x in R:
        d = C3decode(x)
        sys.stdout.write(d)

Decode()

