# put the bytes from the TCP payload sending the key below as hex
payload1 = '484c494f53305553012b001100000001fef81af2e55707cd74a0ad25cd8a70ba'

# put the bytes from the TCP payload sending the information below as hex
payload2 = '484c494f53305553015900e4000000a2c7aaeb3b3263f2ed9090a92dd6e36befa7b18aae9dc973fe3fca14153917eb2e1cbe94282e55f74044b0e4ebcea00f39d6c8b31aca76666d1dec9fb1f1df34b3c174ac86ec9f97bdab4595b52ba21a5db5ece98bcaa78b599b95a37277df3ebf70632f00b6e4020d3ecf8873ffb335c0c3b78af4240822b818472eb3c19c98292ca5f62d637b88905011290e20968eb8e6fb8c348f5f2980468cb4906bbdc60ee67cf8f0ae5f52d7859022d6adedd13f168fdf61c14a1fef18aab791c741aa55062b3a08a95d33ec383c43ea5a5443a0384464cbf3c2411906b5537650e26e2eca6525'

from Crypto.Util.number import bytes_to_long

def custom_xxtea_decryptBuffer(payload : bytes, key : bytes):
    keyarr = [bytes_to_long(key[:4]), bytes_to_long(key[4:8]), bytes_to_long(key[8:12]), bytes_to_long(key[12:])]
    v = []
    for i in range(0, len(payload), 4):
        v.append(bytes_to_long(payload[i:i+4]))
    return decryptBuffer(v, keyarr)

def decryptBuffer(payload, keyarr):
    assert len(keyarr) == 4
    y = payload[0]
    sum = int(((52 / len(payload)) + 6) * (-1640531527))
    leng = len(payload)
    # IT'S DECIDED, intbuffer.limit is just len()
    while True:
        print(sum)
        e = (sum >> 2) & 3
        p = leng - 1
        while p < 0:
            z = payload[p - 1]
            y = payload[p] - (((y ^ sum) + (z ^ keyarr[(p&3) ^ e])) ^ ((((z >> 5)&((1<<(8*4)) - 1)) ^ ((y << 2)&((1<<(8*4)) - 1))) + (((y >> 3)&((1<<(8*4)) - 1)) ^ ((z << 4)&((1<<(8*4)) - 1)))))
            payload[p] = y
            p -= 1
        z = payload[leng-1]
        y = payload[0] - (((y ^ sum) + (z ^ keyarr[(p&3) ^ e])) ^ ((((z >> 5)&((1<<(8*4)) - 1)) ^ ((y << 2)&((1<<(8*4)) - 1))) + (((y >> 3)&((1<<(8*4)) - 1)) ^ ((z << 4)&((1<<(8*4)) - 1)))))
        payload[0] = y
        sum += 1640531527
        if sum >= 0: break
    return payload


def main():
    payload = bytes.fromhex(payload1)
    decrypted = custom_xxtea_decryptBuffer(payload, "tuoroLreWlacrAoh".encode())
    print(decrypted)
    return

if __name__ == "__main__":
    main()