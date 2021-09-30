import codecs

class RC4:
    def __init__(self, key, plaintext):
        self.key = key
        self.plaintext = plaintext
        self.MOD = 256

        self.encrypt()
        self.decrypt()
    
    def KSA(self):
        key_length = len(self.ordKey)
        # create the array "S"
        S = list(range(self.MOD))  # [0,1,2, ... , 255]
        j = 0
        for i in range(self.MOD):
            # print(j)
            # print(S[i])
            # print(self.key[i % key_length])
            j = (j + S[i] + self.ordKey[i % key_length]) % self.MOD
            S[i], S[j] = S[j], S[i]  # swap values

        return S

    def PRGA(self, KSAres):
        i = 0
        j = 0
        while True:
            i = (i + 1) % self.MOD
            j = (j + KSAres[i]) % self.MOD

            KSAres[i], KSAres[j] = KSAres[j], KSAres[i]  # swap values
            K = KSAres[(KSAres[i] + KSAres[j]) % self.MOD]
            yield K

    def get_keystream(self):
        S = self.KSA()
        return self.PRGA(S)

    def encrypt_logic(self, text):
        self.ordKey = [ord(c) for c in self.key]
        keystream = self.get_keystream()

        res = []
        for c in text:
            val = ("%02X" % (c ^ next(keystream)))  # XOR and taking hex
            res.append(val)
        self.encrypted_text = ''.join(res)
        return ''.join(res)

    def encrypt(self):
        plaintext = [ord(c) for c in self.plaintext]
        return self.encrypt_logic(plaintext)

    def decrypt(self):
        ciphertext = codecs.decode(self.encrypted_text, 'hex_codec')
        # print(ciphertext)
        res = self.encrypt_logic(ciphertext)
        self.decrypted_text = codecs.decode(res, 'hex_codec').decode('utf-8')

    def getDecryptedText(self):
        return self.decrypted_text

    def getEncryptedText(self):
        return self.encrypted_text

def main():
    key = 'not-so-random-key'  # plaintext
    plaintext = 'Good work! Your implementation is correct'  # plaintext
    # until next time folks !
    rc4 = RC4(key, plaintext)
    print(rc4.plaintext)
    print(rc4.key)
    print(rc4.encrypted_text)
    print(rc4.decrypted_text)

if __name__ == '__main__':
    main()