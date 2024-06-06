import binascii

SV = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501, 0x698098d8,
      0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821, 0xf61e2562, 0xc040b340,
      0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x2441453, 0xd8a1e681, 0xe7d3fbc8, 0x21e1cde6, 0xc33707d6, 0xf4d50d87,
      0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a, 0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
      0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70, 0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x4881d05, 0xd9d4d039,
      0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, 0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92,
      0xffeff47d, 0x85845dd1, 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb,
      0xeb86d391]


def left_circular_shift(k, bits):
    bits = bits % 32
    k = k % (2 ** 32)
    upper = (k << bits) % (2 ** 32)
    result = upper | (k >> (32 - bits))
    return result


def block_divide(block, chunks):
    result = []
    size = len(block) // chunks
    for i in range(0, chunks):
        result.append(int.from_bytes(block[i * size:(i + 1) * size], "little"))
    return result


def f(x, y, z):
    return (x & y) | ((~x) & z)


def g(x, y, z):
    return (x & z) | (y & (~z))


def h(x, y, z):
    return x ^ y ^ z


def i(x, y, z):
    return y ^ (x | (~z))


def ff(a, b, c, d, m, s, t):
    result = b + left_circular_shift((a + f(b, c, d) + m + t), s)
    return result


def gg(a, b, c, d, m, s, t):
    result = b + left_circular_shift((a + g(b, c, d) + m + t), s)
    return result


def hh(a, b, c, d, m, s, t):
    result = b + left_circular_shift((a + h(b, c, d) + m + t), s)
    return result


def ii(a, b, c, d, m, s, t):
    result = b + left_circular_shift((a + i(b, c, d) + m + t), s)
    return result


def fmt8(num):
    big_hex = "{0:08x}".format(num)
    bin_ver = binascii.unhexlify(big_hex)
    result = "{0:08x}".format(int.from_bytes(bin_ver, 'little'))
    return result


def bit_length(bitstring):
    return len(bitstring) * 8


def md5sum(msg):
    # First, we pad the message
    message_length = bit_length(msg) % (2 ** 64)
    msg = msg + b'\x80'
    zero_pad = (448 - (message_length + 8) % 512) % 512
    zero_pad //= 8
    msg = msg + b'\x00' * zero_pad + message_length.to_bytes(8, 'little')
    message_length = bit_length(msg)
    iterations = message_length // 512
    # chaining variables
    a = 0x67452301
    b = 0xefcdab89
    c = 0x98badcfe
    d = 0x10325476
    # main loop
    for i in range(0, iterations):
        a = a
        b = b
        c = c
        d = d
        block = msg[i * 64:(i + 1) * 64]
        m = block_divide(block, 16)
        # Rounds
        a = ff(a, b, c, d, m[0], 7, SV[0])
        d = ff(d, a, b, c, m[1], 12, SV[1])
        c = ff(c, d, a, b, m[2], 17, SV[2])
        b = ff(b, c, d, a, m[3], 22, SV[3])
        a = ff(a, b, c, d, m[4], 7, SV[4])
        d = ff(d, a, b, c, m[5], 12, SV[5])
        c = ff(c, d, a, b, m[6], 17, SV[6])
        b = ff(b, c, d, a, m[7], 22, SV[7])
        a = ff(a, b, c, d, m[8], 7, SV[8])
        d = ff(d, a, b, c, m[9], 12, SV[9])
        c = ff(c, d, a, b, m[10], 17, SV[10])
        b = ff(b, c, d, a, m[11], 22, SV[11])
        a = ff(a, b, c, d, m[12], 7, SV[12])
        d = ff(d, a, b, c, m[13], 12, SV[13])
        c = ff(c, d, a, b, m[14], 17, SV[14])
        b = ff(b, c, d, a, m[15], 22, SV[15])
        a = gg(a, b, c, d, m[1], 5, SV[16])
        d = gg(d, a, b, c, m[6], 9, SV[17])
        c = gg(c, d, a, b, m[11], 14, SV[18])
        b = gg(b, c, d, a, m[0], 20, SV[19])
        a = gg(a, b, c, d, m[5], 5, SV[20])
        d = gg(d, a, b, c, m[10], 9, SV[21])
        c = gg(c, d, a, b, m[15], 14, SV[22])
        b = gg(b, c, d, a, m[4], 20, SV[23])
        a = gg(a, b, c, d, m[9], 5, SV[24])
        d = gg(d, a, b, c, m[14], 9, SV[25])
        c = gg(c, d, a, b, m[3], 14, SV[26])
        b = gg(b, c, d, a, m[8], 20, SV[27])
        a = gg(a, b, c, d, m[13], 5, SV[28])
        d = gg(d, a, b, c, m[2], 9, SV[29])
        c = gg(c, d, a, b, m[7], 14, SV[30])
        b = gg(b, c, d, a, m[12], 20, SV[31])
        a = hh(a, b, c, d, m[5], 4, SV[32])
        d = hh(d, a, b, c, m[8], 11, SV[33])
        c = hh(c, d, a, b, m[11], 16, SV[34])
        b = hh(b, c, d, a, m[14], 23, SV[35])
        a = hh(a, b, c, d, m[1], 4, SV[36])
        d = hh(d, a, b, c, m[4], 11, SV[37])
        c = hh(c, d, a, b, m[7], 16, SV[38])
        b = hh(b, c, d, a, m[10], 23, SV[39])
        a = hh(a, b, c, d, m[13], 4, SV[40])
        d = hh(d, a, b, c, m[0], 11, SV[41])
        c = hh(c, d, a, b, m[3], 16, SV[42])
        b = hh(b, c, d, a, m[6], 23, SV[43])
        a = hh(a, b, c, d, m[9], 4, SV[44])
        d = hh(d, a, b, c, m[12], 11, SV[45])
        c = hh(c, d, a, b, m[15], 16, SV[46])
        b = hh(b, c, d, a, m[2], 23, SV[47])
        a = ii(a, b, c, d, m[0], 6, SV[48])
        d = ii(d, a, b, c, m[7], 10, SV[49])
        c = ii(c, d, a, b, m[14], 15, SV[50])
        b = ii(b, c, d, a, m[5], 21, SV[51])
        a = ii(a, b, c, d, m[12], 6, SV[52])
        d = ii(d, a, b, c, m[3], 10, SV[53])
        c = ii(c, d, a, b, m[10], 15, SV[54])
        b = ii(b, c, d, a, m[1], 21, SV[55])
        a = ii(a, b, c, d, m[8], 6, SV[56])
        d = ii(d, a, b, c, m[15], 10, SV[57])
        c = ii(c, d, a, b, m[6], 15, SV[58])
        b = ii(b, c, d, a, m[13], 21, SV[59])
        a = ii(a, b, c, d, m[4], 6, SV[60])
        d = ii(d, a, b, c, m[11], 10, SV[61])
        c = ii(c, d, a, b, m[2], 15, SV[62])
        b = ii(b, c, d, a, m[9], 21, SV[63])
        a = (a + a) % (2 ** 32)
        b = (b + b) % (2 ** 32)
        c = (c + c) % (2 ** 32)
        d = (d + d) % (2 ** 32)
    result = fmt8(a) + fmt8(b) + fmt8(c) + fmt8(d)
    return result

def md5sum_file(filepath):
    with open(filepath, "rb") as f:
        return md5sum(f.read())

def test():
    data = str("Secret Message").encode("UTF-8")
    print("str2hash: ", data)
    print(md5sum(data))


if __name__ == "__main__":
    test()
