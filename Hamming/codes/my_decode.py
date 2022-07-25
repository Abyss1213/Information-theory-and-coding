import sys
import numpy as np


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
    l = len(r)
    for i in range(0, l, 15):
        d = C3decode(r[i:15 + i])
        sys.stdout.write(d)

Decode()

