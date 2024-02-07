# put the bytes from the TCP payload sending the key below as hex
payload1 = '484c494f53305553012b001100000001fef81af2e55707cd74a0ad25cd8a70ba'

# put the bytes from the TCP payload sending the information below as hex
payload2 = '484c494f53305553015900e4000000a2c7aaeb3b3263f2ed9090a92dd6e36befa7b18aae9dc973fe3fca14153917eb2e1cbe94282e55f74044b0e4ebcea00f39d6c8b31aca76666d1dec9fb1f1df34b3c174ac86ec9f97bdab4595b52ba21a5db5ece98bcaa78b599b95a37277df3ebf70632f00b6e4020d3ecf8873ffb335c0c3b78af4240822b818472eb3c19c98292ca5f62d637b88905011290e20968eb8e6fb8c348f5f2980468cb4906bbdc60ee67cf8f0ae5f52d7859022d6adedd13f168fdf61c14a1fef18aab791c741aa55062b3a08a95d33ec383c43ea5a5443a0384464cbf3c2411906b5537650e26e2eca6525'


### DON'T TOUCH ANYTHING BELOW THIS LINE ###
import xxtea, subprocess, binascii

# helper function (symmetric, so it can both deobfuscate and obfuscate)
def obfuscate(b_arr : bytes):
    retval = bytearray(16)
    for i in range(4):
        retval[i] = b_arr[3 - i]
        retval[i + 4] = b_arr[7 - i]
        retval[i + 8] = b_arr[11 - i]
        retval[i + 12] = b_arr[15 - i]
    return bytes(retval)

bytes_from_server = bytes.fromhex(payload1)[16:]
original_key = b'routerLocalWhoAr'

encrypted = obfuscate(bytes_from_server)
key = obfuscate(original_key)
print("ENCRYPTED:", encrypted)
print("KEY:", key)

out = xxtea.decrypt(encrypted, key)
print(out)

# out = xxtea.encrypt(b"testMessage123\xbc", key)
# print(out)
# out = xxtea.decrypt(out, key)
# print(out)

# get output
# new_key = deobfuscate(bytes.fromhex(out))
# second_payload = bytes.fromhex(payload2)[15:]
# print(xxtea.decrypt(second_payload, new_key))