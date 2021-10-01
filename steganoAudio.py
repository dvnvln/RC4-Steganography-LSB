import os
import wave

class SteganoAudio:
    def __init__(self, audioPath=None):
        if(audioPath != None):
            self.audioPath = audioPath

            self.audioFile = wave.open(self.audioPath, mode='rb')
            self.frame_bytes = bytearray(list(self.audioFile.readframes(self.audioFile.getnframes())))

            self.modified_frame = self.frame_bytes
            self.embeddedOutputPath = self.audioPath.split(".")[0] + '_embedded.wav'

    def embeddingLSB(self, text):
        self.text = text
        hashEmbed = int((len(self.frame_bytes) - (len(text)*8*8))/8) * '#'
        self.text += hashEmbed
        
        self.bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in self.text])))
        
        for i, bit in enumerate(self.bits):
            self.frame_bytes[i] = (self.frame_bytes[i] & 254) | bit
        self.modified_frame = bytes(self.frame_bytes)

        with wave.open(self.embeddedOutputPath, 'wb') as fd:
            fd.setparams(self.audioFile.getparams())
            fd.writeframes(self.modified_frame)
    
    def textExtraction(self, audioFilePath):
        self.audioFile = wave.open(audioFilePath, mode='rb')
        self.frame_bytes = bytearray(list(self.audioFile.readframes(self.audioFile.getnframes())))

        self.extractedText = [self.frame_bytes[i] & 1 for i in range(len(self.frame_bytes))]
        self.extractedText = ''.join(chr(int(''.join(map(str, self.extractedText[i:i+8])), 2)) for i in range(0, len(self.extractedText), 8))
        self.extractedText = self.extractedText.split('###')[0]

def main():
    stegano = SteganoAudio("sampleStego.wav")
    stegano.embeddingLSB("hai sayang")
    stegano2 = SteganoAudio()
    stegano2.textExtraction("sampleStego_embedded.wav")
    print(stegano2.extractedText)
    # print(stegano.extractedText)
    # print(stegano.modified_frame)
    # print(stegano.secretText)

if __name__ == '__main__':
    main()