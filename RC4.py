class RC4 :
    def __init__(self) :
        self.S1 = []
        self.S2 = []

    def KSA(self, key_1, key_2) :
        self.S1 = [i for i in range(256)]
        self.S2 = [(256-i-1) for i in range(256)]

        j1 = 0
        j2 = 0
        for i in range(256) :
            j1 = (j1 + self.S1[i] + ord(key_1[i % len(key_1)])) % 256
            j2 = (j2 + self.S2[i] + ord(key_2[i % len(key_2)])) % 256

            temp = self.S1[i]
            self.S1[i] = self.S1[j1]
            self.S1[j1] = temp

            self.S2[i], self.S2[j2] = self.S2[j2], self.S2[i]

        vector = ''
        i = 0
        j = 0
        vector += chr(ord(key_1[i % len(key_1)]) ^ ord(key_2[j % len(key_2)]))
        while i != len(key_1)-1 or j != len(key_2)-1 :
            i = (i + 1) % len(key_1)
            j = (j + 1) % len(key_2)
            vector += chr(ord(key_1[i % len(key_1)]) ^ ord(key_2[j % len(key_2)]))

        j1 = 0
        j2 = 0

        for i in range(256//2) :
            modTemp = 256//2-i-1
            ord1 = ord(key_1[modTemp % len(key_1)])
            ord2 = ord(key_2[modTemp % len(key_2)])
            ordVec = ord(vector[modTemp % len(vector)])

            j1 = ((j1 + self.S1[modTemp]) ^ (ord1 + ordVec)) % 256
            j2 = ((j2 + self.S2[modTemp]) ^ (ord2 + ordVec)) % 256
            self.S1[modTemp], self.S1[j1] = self.S1[j1], self.S1[modTemp]
            self.S2[modTemp], self.S2[j2] = self.S2[j2], self.S2[modTemp]

        for i in range(256//2, 256) :
            modTemp = 256//2-i-1
            ord1 = ord(key_1[i % len(key_1)])
            ord2 = ord(key_2[i % len(key_2)])
            ordVec = ord(vector[i % len(vector)])
            
            j1 = ((j1 + self.S1[i]) ^ (ord1 + ordVec)) % 256
            j2 = ((j2 + self.S2[i]) ^ (ord2 + ordVec)) % 256
            self.S1[i], self.S1[j1] = self.S1[j1], self.S1[i]
            self.S2[i], self.S2[j2] = self.S2[j2], self.S2[i]

        j1 = 0
        j2 = 0
        for count in range(256) :
            i = count//2 if count % 2 == 0 else 256-(count+1)//2
            ord1 = ord(key_1[i % len(key_1)])
            ord2 = ord(key_2[i % len(key_2)])

            j1 = (j1 + self.S1[i] + ord1) % 256
            j2 = (j2 + self.S2[i] + ord2) % 256
            self.S1[i], self.S1[j1] = self.S1[j1], self.S1[i]
            self.S2[i], self.S2[j2] = self.S2[j2], self.S2[i]

    def PRGA(self, plaintext) :
        keystream = ''
        i = 0
        j1 = 0
        j2 = 0
        for idx in range(len(plaintext)) :
            i = (i + 1) % 256
            j1 = (j1 + self.S1[i]) % 256
            j2 = (j2 + self.S2[i]) % 256
            self.S1[i], self.S1[j1] = self.S1[j1], self.S1[i]
            self.S2[i], self.S2[j2] = self.S2[j2], self.S2[i]
            t = ((self.S1[i] + self.S1[j1]) + (self.S2[i] + self.S2[j2])) % 256
            keystream += chr(self.S1[t] ^ self.S2[t])

        return keystream

    def encrypt(self, plaintext, key_1, key_2) :
        ciphertext = ''

        self.KSA(key_1, key_2)
        keystream = self.PRGA(plaintext)
        for idx in range(len(plaintext)) :
            c = chr(ord(keystream[idx]) ^ ord(plaintext[idx]))
            ciphertext += c if c.isprintable() else r'\x{0:02x}'.format(ord(c))

        return ciphertext

    def encrypt_binary(self, plaintext, key_1, key_2) :
        ciphertext = []

        self.KSA(key_1, key_2)
        keystream = self.PRGA(plaintext)
        for idx in range(len(plaintext)) :
            c = ord(keystream[idx]) ^ plaintext[idx]
            ciphertext.append(c)

        return ciphertext

    def decrypt(self, ciphertext, key_1, key_2) :
        hexToAscii = ''

        i = 0
        while i < len(ciphertext) :
            if '\\x' == ciphertext[i:i+2] :
                c = int(ciphertext[i+2:i+4], base=16)
                hexToAscii += chr(c)
                i += 4
            else :
                hexToAscii += ciphertext[i]
                i += 1

        ciphertext = hexToAscii

        plaintext = ''

        self.KSA(key_1, key_2)
        keystream = self.PRGA(ciphertext)
        for idx in range(len(ciphertext)) :
            p = chr(ord(keystream[idx]) ^ ord(ciphertext[idx]))
            plaintext += p if p.isprintable() else r'\x{0:02x}'.format(ord(p))

        return plaintext

    def decrypt_binary(self, ciphertext, key_1, key_2) :
        plaintext = []

        self.KSA(key_1, key_2)
        keystream = self.PRGA(ciphertext)
        for idx in range(len(ciphertext)) :
            p = ord(keystream[idx]) ^ ciphertext[idx]
            plaintext.append(p)

        return plaintext

# mrc4 = RC4()
# key_1 = "hakim"
# key_2 = "ipul"
# cip = mrc4.encrypt("kriptografi sangat menyenangkan", key_1, key_2)
# # <b\x80_dî\x81,ew\xadPò/+Ù«8ÉZ¼3\x8dÖª~ùUÛö©
# print(cip)
# pla = mrc4.decrypt(cip, key_1, key_2)
# print(pla)