import numpy as np
import difflib
from random import randint


H = np.zeros((15, 4))
for i in range(15):
    tmp = bin(i+1)[2:].zfill(4)
    H[i] = np.matrix([int(tmp[3]), int(tmp[2]), int(tmp[1]), int(tmp[0])], dtype = np.int32)
H = H.T

G = [[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
     [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
     [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
     [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
     [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
     [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
     [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]]



def str2list(s:str):
    res = []
    for i in range(15):
        res.append([])
        res[i].append(int(s[i]))
    return res


def list2int(z:list):  # 看哪位出错
    res = ''
    for i in range(4):
        res += str(int(z[i]) % 2)
    res = res[::-1]
    res = int(res, 2)
    return res


def C1encode(s:int):
    tmp = bin(s)[2:].zfill(11)[::-1]
    d = [[]]
    for i in range(11):
        d[0].append(int(tmp[i]))
    res = np.dot(d, G)
    out = ''
    for x in res[0]:
        out += str(x % 2)
    return out


def C1decode(r: str):
    R = str2list(r)
    z = np.dot(H, R)
    tmp = list2int(z)
    if tmp != 0:
        R[tmp-1][0] = ~R[tmp-1][0] % 2
    r = ''
    for i in range(15):
        r += str(R[i][0])
    res = r[2]+r[4:7]+r[8:]
    return res


def C3encode(d: str):
    D = '0'+'0'+d[0]+'0'+d[1:4]+'0'+d[4:]
    b = 0
    for i in range(15):
        if D[i] == '1':
            b ^= i+1
    p = bin(b)[2:].zfill(4)[::-1]
    r = p[0] + p[1] + d[0] + p[2] + d[1:4] + p[3] + d[4:]
    return r


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


def vrfy_encode():
    with open('C3_Hamming_encode.txt', 'w') as f:
        for i in range(2048):
            i = bin(i)[2:].zfill(11)[::-1]
            tmp = C3encode(i)
            f.writelines(i+', '+tmp+'\n')
    f1 = open('C3_Hamming_encode.txt', 'r')
    f2 = open('hamming_15_11.txt', 'r')
    txt1 = f1.read().splitlines()
    txt2 = f2.read().splitlines()
    d = difflib.HtmlDiff()
    htmlContent = d.make_file(txt1,txt2)
    print(htmlContent)
    with open('C3EncodeDiff.html','w') as f3:
        f3.write(htmlContent)
    f1.close()
    f2.close()


def vrfy_decode():
    f1 = open('C3_origin.txt', 'w')
    f2 = open('C3_decode_res.txt', 'w')
    for i in range(2048):
        i = bin(i)[2:].zfill(11)[::-1]
        f1.writelines(i+'\n')
        r = C3encode(i)
        d = C3decode(r)
        f2.writelines(d + '\n')
    f1.close()
    f2.close()
    f1 = open('C3_origin.txt', 'r')
    f2 = open('C3_decode_res.txt', 'r')
    txt1 = f1.read().splitlines()
    txt2 = f2.read().splitlines()
    d = difflib.HtmlDiff()
    htmlContent = d.make_file(txt1, txt2)
    print(htmlContent)
    with open('C3DecodeDiff.html', 'w') as f3:
        f3.write(htmlContent)
    f1.close()
    f2.close()


def vrfy_correct():
    f = open('C3_correct.txt','w')
    for i in range(2048):
        i = bin(i)[2:].zfill(11)[::-1]
        r = C3encode(i)
        w = randint(0, 14)
        if r[w] == '0':
            r = r[0:w] + '1' + r[w+1:]
        else:
            r = r[0:w] + '0' + r[w + 1:]
        d = C3decode(r)
        f.writelines(d + '\n')
    f.close()
    f1 = open('C3_correct.txt', 'r')
    f2 = open('C3_decode_res.txt', 'r')
    txt1 = f1.read().splitlines()
    txt2 = f2.read().splitlines()
    d = difflib.HtmlDiff()
    htmlContent = d.make_file(txt1, txt2)
    print(htmlContent)
    with open('C3CorrectDiff.html', 'w') as f3:
        f3.write(htmlContent)
    f1.close()
    f2.close()


vrfy_encode()
vrfy_decode()
vrfy_correct()
