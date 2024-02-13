from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto import Random
from base64 import b64encode

BLOCKSIZE = 8

# def encrypt(num_rounds, plaintext, key, iv):
#     pt = pad(plaintext.encode(), 8)
#     ct = b''
#     curriv = iv
#     for i in range(0, len(pt), 8):
#         roundpt = bytes([b1 ^ b2 for b1, b2 in zip(pt[i:i+8], curriv)])
#         round = scramble(num_rounds, roundpt, key)
#         ct += round
#         curriv = round
#     return ct

def deobfuscate(b_arr : bytes):
    retval = bytearray(16)
    for i in range(4):
        retval[i] = b_arr[3 - i]
        retval[i + 4] = b_arr[7 - i]
        retval[i + 8] = b_arr[11 - i]
        retval[i + 12] = b_arr[15 - i]
    return bytes(retval)

def package(flag : int, ciphertext : bytes, key : bytes):
    ctarr = []
    keyarr = []
    for i in range(0, len(ciphertext), 4):
        ctarr.append(bytes_to_long(ciphertext[i:i+4]))
    for i in range(0, len(key), 4):
        keyarr.append(bytes_to_long(key[i:i+4]))
    print(len(ctarr))
    decrypted = decrypt_xxtea(ctarr, len(ctarr), keyarr)
    pt = b''
    for i in decrypted:
        pt += long_to_bytes(i)
    return pt


def decrypt_xxtea(v, n, key):
    delta = 0x61c88647
    q = 0x34 // n + 6
    summed = q * (-1 * delta)
    y = v[0]
    if (n-1 != 0):
        while summed != 0:
            e = (summed >> 2) & 3
            for p in range(n-1, 0, -1):
                z = v[p-1]
                v[p] = v[p] - (((z >> 5)&((1<<(8*4)) - 1) ^ (y << 2)&((1<<(8*4)) - 1)) + ((y >> 3)&((1<<(8*4)) - 1) ^ (z << 4)&((1<<(8*4)) - 1)) ^ (summed ^ y) + key[p&3^e] ^ z)
                y = v[p]
            z = v[n-1]
            v[0] = v[0] - (((z >> 5)&((1<<(8*4)) - 1) ^ (y << 2)&((1<<(8*4)) - 1)) + ((y >> 3)&((1<<(8*4)) - 1) ^ (z << 4)&((1<<(8*4)) - 1)) ^ (summed ^ y) + key[p&3^e] ^ z)
            y = v[0]
            summed += delta
    return v

def dec(payload1, payload2):
    # put the bytes from the TCP payload sending the key below as hex
    #payload1 = ''

    # put the bytes from the TCP payload sending the information below as hex
    #payload2 = ''


    ### DON'T TOUCH ANYTHING BELOW THIS LINE ###
    import xxtea, subprocess, binascii

    # helper function
    def deobfuscate(b_arr : bytes):
        retval = bytearray(16)
        for i in range(4):
            retval[i] = b_arr[3 - i]
            retval[i + 4] = b_arr[7 - i]
            retval[i + 8] = b_arr[11 - i]
            retval[i + 12] = b_arr[15 - i]
        return bytes(retval)

    # get payload for Java file
    original_key = b'routerLocalWhoAr'
    bytes_from_server = bytes.fromhex(payload1)[16:]
    arg = binascii.hexlify(deobfuscate(bytes_from_server)).decode('utf-8')
    print(arg)

    # subprocess
    out = subprocess.getoutput(f'javac pain.java && java pain {arg}')
    
    print(out)
    # get output
    new_key = deobfuscate(bytes.fromhex(out))
    second_payload = bytes.fromhex(payload2)[15:]
    return xxtea.decrypt(second_payload, new_key)


def main():
    # put the bytes from the TCP payload sending the key below as hex
    payload1 = '484c494f53305553012b001100000001fef81af2e55707cd74a0ad25cd8a70ba'

    # put the bytes from the TCP payload sending the information below as hex
    payload2 = '484c494f53305553015900e4000000a2c7aaeb3b3263f2ed9090a92dd6e36befa7b18aae9dc973fe3fca14153917eb2e1cbe94282e55f74044b0e4ebcea00f39d6c8b31aca76666d1dec9fb1f1df34b3c174ac86ec9f97bdab4595b52ba21a5db5ece98bcaa78b599b95a37277df3ebf70632f00b6e4020d3ecf8873ffb335c0c3b78af4240822b818472eb3c19c98292ca5f62d637b88905011290e20968eb8e6fb8c348f5f2980468cb4906bbdc60ee67cf8f0ae5f52d7859022d6adedd13f168fdf61c14a1fef18aab791c741aa55062b3a08a95d33ec383c43ea5a5443a0384464cbf3c2411906b5537650e26e2eca6525'

    bytes_from_server = bytes.fromhex(payload1)[16:] # memcpy actually cuts the first 15 bytes, too
    original_key = b'routerLocalWhoAr'
    print(package(0, deobfuscate(bytes_from_server), original_key))

    # print(dec('484c494f53305553012b001100000001fef81af2e55707cd74a0ad25cd8a70ba', '484c494f53305553015900e4000000a2c7aaeb3b3263f2ed9090a92dd6e36befa7b18aae9dc973fe3fca14153917eb2e1cbe94282e55f74044b0e4ebcea00f39d6c8b31aca76666d1dec9fb1f1df34b3c174ac86ec9f97bdab4595b52ba21a5db5ece98bcaa78b599b95a37277df3ebf70632f00b6e4020d3ecf8873ffb335c0c3b78af4240822b818472eb3c19c98292ca5f62d637b88905011290e20968eb8e6fb8c348f5f2980468cb4906bbdc60ee67cf8f0ae5f52d7859022d6adedd13f168fdf61c14a1fef18aab791c741aa55062b3a08a95d33ec383c43ea5a5443a0384464cbf3c2411906b5537650e26e2eca6525'))    

if __name__ == "__main__":
    main()
