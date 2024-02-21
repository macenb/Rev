import ctypes
from Crypto.Util.Padding import pad
import xxtea

u32 = ctypes.c_uint32
DELTA = 0x9e3779b9

# this doesn't work yet
def encrypt(v, n, k):
    # v is array of uint32_t, n is ssize_t, k is array of uint32_t
    q = u32(6 + 52//n.value)
    sum = u32(0)
    z = v[n.value - 1].value
    for q1 in range(q.value-1, 0, -1):
        sum = u32(sum.value + DELTA)
        e = (sum.value >> 2) & 3
        for p1 in range(0, n.value-1):
            y = v[p1+1].value
            z = v[p1].value
            v[p1].value = u32(v[p1].value + (u32((z>>5^u32(y<<2).value) + (y>>3^u32(z<<4).value)).value ^ u32((sum.value^y) + (k[p1&3^e].value^z)).value)).value
        y = v[0].value
        z = v[n.value-1].value
        v[n.value-1].value = u32(v[n.value-1].value + (u32((z>>5^u32(y<<2).value) + (y>>3^u32(z<<4).value)).value ^ u32((sum.value^y) + (k[p1&3^e].value^z)).value)).value
    return b''.join([int.to_bytes(x.value, 4) for x in v])


def main(text, key):
    # plaintext = pad(text, 4)
    # print(plaintext)
    v = []
    for i in range(0, len(text), 4):
        v.append(u32(int.from_bytes(text[i:i+4], "big")))
    k = []
    for i in range(0, len(key), 4):
        k.append(u32(int.from_bytes(key[i:i+4], "big")))
    home_encrypted = encrypt(v, u32(len(v)), k)
    encrypted = xxtea.encrypt(text, key)
    print(home_encrypted)
    print(encrypted)

if __name__ == "__main__":
    plaintext = b"abcdefghijklmnop"
    key = b'routerLocalWhoAr'
    main(plaintext, key)
    