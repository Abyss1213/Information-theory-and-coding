def OP4encode(d: str):
    D = '0'+'0'+d[0]+'0'+d[1:4]+'0'+d[4:]
    b = 0
    for i in range(15):
        if D[i] == '1':
            b ^= i+1
    p = bin(b)[2:].zfill(4)[::-1]
    r = p[0] + p[1] + d[0] + p[2] + d[1:4] + p[3] + d[4:]
    count = 0
    for x in r:
        if x == '1':
            count += 1
    if count % 2 == 1:
        r = r + '1'
    else:
        r = r + '0'
    return r


def OP4decode(r: str):
    b = 0
    for i in range(15):
        if r[i] == '1':
            b ^= i+1
    if b != 0:
        if r[15] == '1':
            print('one error')
            if r[b-1] == '0':
                r = r[0:b-1] + '1' + r[b:15]
            else:
                r = r[0:b-1] + '0' + r[b:15]
        else:
            return 'two errors'
    else:
        if r[15] == '1':
            print('总校验位出错，直接提取数据')
        else:
            print('no error')
    d = r[2]+r[4:7]+r[8:15]
    return d


def test():
    print('encode test:')
    a = '10100000000'
    print('need: 1011010000000000')
    print('got: ', OP4encode(a), '\n')

    print('decode test:')
    b = '1011010000000000'
    print('need: 10100000000')
    print('got: ', OP4decode(b), '\n')

    print('one error test:')
    c = '1001010000000001'
    print('need: 10100000000')
    print('got: ', OP4decode(c), '\n')

    print('two errors test:')
    d = '1000010000000000'
    print('need: two errors')
    print('got: ', OP4decode(d))


test()

