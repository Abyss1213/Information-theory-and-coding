import os
from queue import PriorityQueue
import math
import struct

class HuffmanNode(object):
    def __init__(self, value, key=None, symbol='', left_child=None, right_child=None):
        self.left_child = left_child
        self.right_child = right_child
        self.value = value
        self.key = key
        assert symbol == ''
        self.symbol = symbol

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value


def createTree(hist_dict: dict) -> HuffmanNode:
    # 借助优先级队列实现直方图频率的排序，取出和插入元素很方便
    q = PriorityQueue()

    # 根据传入的像素值和频率字典构造哈夫曼节点并放入队列中
    for k, v in hist_dict.items():
        # 这里放入的都是之后哈夫曼树的叶子节点，key都是各自的元素
        q.put(HuffmanNode(value=v, key=k))

    # 判断条件，直到队列中只剩下一个根节点
    while q.qsize() > 1:
        # 取出两个最小的哈夫曼节点，队列中这两个节点就不在了
        l_freq, r_freq = q.get(), q.get()
        # 增加他们的父节点，父节点值为这两个哈夫曼节点的和，但是没有key值；左子节点是较小的，右子节点是较大的
        node = HuffmanNode(value=l_freq.value + r_freq.value, left_child=l_freq, right_child=r_freq)
        # 把构造的父节点放在队列中，继续排序和取放、构造其他的节点
        q.put(node)

    # 队列中只剩下根节点了，返回根节点
    return q.get()


def walkTree(root_node: HuffmanNode, symbol=''):
    # 为了不增加变量复制的成本，直接使用一个dict类型的全局变量保存每个元素对应的哈夫曼编码
    global Huffman_encode_dict

    # 判断节点是不是HuffmanNode，因为叶子节点的子节点是None
    if isinstance(root_node, HuffmanNode):
        # 编码操作，改变每个子树的根节点的哈夫曼编码，根据遍历过程是逐渐增加编码长度到完整的
        root_node.symbol += symbol
        # 判断是否走到了叶子节点，叶子节点的key!=None
        if root_node.key != None:
            # 记录叶子节点的编码到全局的dict中
            Huffman_encode_dict[root_node.key] = root_node.symbol

        # 访问左子树，左子树在此根节点基础上赋值'0'
        walkTree(root_node.left_child, symbol=root_node.symbol + '0')
        # 访问右子树，右子树在此根节点基础上赋值'1'
        walkTree(root_node.right_child, symbol=root_node.symbol + '1')

    return


def writeBinFile(file_encode: str, huffman_file_name: str, p: int):
    # 以huf后缀标志该程序编码文件
    with open(huffman_file_name + '.huf', 'wb') as f:
        # 存补的字节数
        f.write(struct.pack('i', p))
        # 存编码字符串长度,这里只用了4字节存，编码长度不可超过2^32
        file_encode_len = len(file_encode)
        file_encode_len_bin = struct.pack('i', file_encode_len)
        f.write(file_encode_len_bin)
        # 用4字节存字典长度
        dict_len = len(Huffman_encode_dict)
        dict_len_bin = struct.pack('i', dict_len)
        f.write(dict_len_bin)
        # 写入字典
        k = Huffman_encode_dict.keys()
        v = Huffman_encode_dict.values()
        l = []  # 存编码长度
        int_v = []  # 存十进制编码
        for val in v:
            l.append(len(val))
            int_v.append(int(val, 2))
        # 存键
        for key in k:
            f.write(key)
        # 存编码长度
        for lenth in l:
            len_bin = struct.pack('B', lenth)
            f.write(len_bin)
        # 存编码，用4字节打包编码，防止不够
        for i in int_v:
            i_bin = struct.pack('i', i)
            f.write(i_bin)

        # 每8个bit组成一个byte。反正存十进制，这里最后不用补位。
        for i in range(0, len(file_encode), 8):
            # 把这一个字节的数据根据二进制翻译为十进制的数字
            file_encode_dec = int(file_encode[i:i + 8], 2)
            # 把这一个字节的十进制数据打包为一个unsigned char，大端（可省略）
            file_encode_bin = struct.pack('>B', file_encode_dec)
            # 写入这一个字节数据
            f.write(file_encode_bin)


def readBinFile(huffman_file_path: str):
    code_bin_str = ""
    # 读二进制数据
    with open(huffman_file_path, 'rb') as f:
        # 跳过补的字节数数据
        f.seek(4, 0)
        file_encode_len = struct.unpack('i', f.read(4))[0]
        # print(file_encode_len)
        dict_len = struct.unpack('i', f.read(4))[0]
        # 跳到编码内容
        f.seek(12 + 6 * dict_len, 0)
        content = f.read()
        # print(content)
        # 从二进制数据解包到十进制数据，所有数据组成的是tuple
        code_dec_tuple = struct.unpack('>' + 'B' * len(content), content)
        for code_dec in code_dec_tuple:
            # 通过bin把解压的十进制数据翻译为二进制的字符串，并填充为8位，否则会丢失高位的0
            # 0 -> bin() -> '0b0' -> [2:] -> '0' -> zfill(8) -> '00000000'
            # print(code_dec)
            code_bin_str += bin(code_dec)[2:].zfill(8)
            # print(code_bin_str)
        # 由于原始的编码最后可能不足8位，保存到一个字节的时候会在高位自动填充0，读取的时候需要去掉填充的0，否则读取出的编码会比原来的编码长
        # 计算读取的编码字符串与原始编码字符串长度的差，差出现在读取的编码字符串的最后一个字节，去掉高位的相应数量的0就可以
        len_diff = len(code_bin_str) - file_encode_len
        # 在读取的编码字符串最后8位去掉高位的多余的0，因为写进去的时候也没补
        code_bin_str = code_bin_str[:-8] + code_bin_str[-(8 - len_diff):]
    return code_bin_str


def encodeFile(src_file: list, encode_dict: dict):
    file_encode = ""
    for i in src_file:
        file_encode += encode_dict[i]
    # print('!', src_file, len(src_file))
    return file_encode


def decodeFile(file_encode: str, encode_dict: dict):
    print(file_encode)
    file_src_val = b''
    decode_dict = {}
    # 构造一个key-value互换的字典，i.e. dict={code:element}，后边方便使用
    for k, v in encode_dict.items():
        decode_dict[v] = k
    # s用来记录当前字符串的访问位置，相当于一个指针
    s = 0
    # 只要没有访问到最后
    while len(file_encode) > s:
        # 遍历字典中每一个键code
        for k in decode_dict.keys():
            # 如果当前的code字符串与编码字符串前k个字符相同，k表示code字符串的长度，那么就可以确定这k个编码对应的元素是什么
            if k == file_encode[s:s + len(k)]:
                #file_src_val.append(decode_dict[k])
                file_src_val += decode_dict[k]
                # print(s, file_src_val)
                # 指针移动k个单位
                s += len(k)
                # 如果已经找到了相应的编码了，就可以找下一个了
                break
    # print('!', file_src_val, len(file_src_val))
    return file_src_val


# 将字节流按n为一组分组成字节型列表，最后一组不够用\x00补齐
def padding(byte, n):
    res = []
    l = len(byte)
    m = l % n
    p = n - m  # 需要补充的字节数
    for i in range(p):
        byte += b'\x00'
    for i in range(0, l, n):
        res.append(byte[i: i+n])
    return res


def encode(path, file_name, n):
    with open(path, 'rb') as fin:
        file_data = fin.read()
        # print('原文件内容:', file_data)
    file_size = len(file_data)
    file_data = padding(file_data, n)
    hist_dict = {}
    for p in file_data:
        if p not in hist_dict:
            hist_dict[p] = 1
        else:
            hist_dict[p] += 1

    # 构造哈夫曼树
    huffman_root_node = createTree(hist_dict)
    # 遍历哈夫曼树，并得到每个元素的编码，保存到Huffman_encode_dict,这是全局变量
    walkTree(huffman_root_node)
    global Huffman_encode_dict
    # 考虑文件只有一种字节的情况
    if len(hist_dict) == 1:
        for key in Huffman_encode_dict:
            Huffman_encode_dict[key] = '0'
        file_encode = ''
        for i in range(file_size):
            file_encode += '0'
    else:
        file_encode = encodeFile(file_data, Huffman_encode_dict)
    print('哈夫曼编码字典：', Huffman_encode_dict)
    print('编码结果:', file_encode, len(file_encode))
    p = n - file_size % n
    writeBinFile(file_encode, file_name, p)

    # 计算平均编码长度和编码效率
    total_code_num = sum(hist_dict.values())
    avg_code_len = 0
    I_entropy = 0
    for key in hist_dict.keys():
        count = hist_dict[key]
        code_len = len(Huffman_encode_dict[key])
        prob = count / total_code_num
        avg_code_len += prob * code_len
        I_entropy += -(prob * math.log2(prob))
    S_eff = I_entropy / avg_code_len
    print("平均编码长度为：{:.3f}".format(avg_code_len))
    print("编码效率为：{:.6f}".format(S_eff))

    # 压缩率
    ori_size = file_size * 8 / (1024 * 8)
    comp_size = len(file_encode) / (1024 * 8) + (12 + 6 * len(Huffman_encode_dict)) / 1024
    comp_rate = 1 - comp_size / ori_size
    print('原文件大小', ori_size, 'KB  压缩后大小(带字典)', comp_size, 'KB  压缩率', comp_rate * 100, '%')


def decode(path, file_name, n):
    with open(path, 'rb') as f:
        if os.path.splitext(path)[-1] == '.huf':
            # 读补码长度
            p = struct.unpack('i', f.read(4))[0]
            # 读编码内容
            file_encode = readBinFile(path)
            # print(file_encode)
            # 用于跳过前8字节的补码长度和编码长度
            f.seek(8, 0)
            # 读字典长度
            dict_len = struct.unpack('i', f.read(4))[0]
            # 读键
            key_decode = []
            for i in range(dict_len):
                key_decode.append(f.read(n))
            # 读编码长度
            len_decode = []
            for i in range(dict_len):
                lenth = struct.unpack('B', f.read(1))[0]
                len_decode.append(lenth)
            # 读编码
            code_dec = []
            for i in range(dict_len):
                code = struct.unpack('i', f.read(4))[0]
                code_dec.append(code)
            # 将编码恢复成二进制
            value_decode = []
            for i in range(dict_len):
                value_decode.append(bin(code_dec[i])[2:].zfill(len_decode[i]))
            # 恢复字典
            Huffman_encode_dict = dict(zip(key_decode, value_decode))
            # print(Huffman_encode_dict)
            # print('原文件编码:', file_encode)
            print('哈夫曼字典：', Huffman_encode_dict)
            # 根据编码字典进行解码的方式
            file_src_val_array = decodeFile(file_encode, Huffman_encode_dict)
            res_file = open(file_name, 'wb')
            for i in range(len(file_src_val_array) - p):
                res_file.write(bytes(file_src_val_array[i]))
            # print(file_src_val_array)
            res_file.close()
            # print('译码结果：', file_src_val_array)
        else:
            print('待译码文件非本程序编码，请重新输入路径')
            return


if __name__ == '__main__':
    # 哈夫曼编码字典{byte_value:code}，在函数中作为全局变量用到
    Huffman_encode_dict = {}
    m = int(input('请输入模式：（1 编码；0 译码） '))
    n = int(input('请输入以多少字节为一组进行编/译码：'))
    path = input('请输入待处理文件路径：')
    if os.path.getsize(path):
        if m == 1:
            file_name = input('请输入编码后文件名：')
            encode(path, file_name, n)
        else:
            file_name = input('请输入译码后文件名（包括后缀）：')
            decode(path, file_name, n)
            print('译码完成，请查看' + file_name)
    else:
        print('输入文件为空，请重新输入路径')
