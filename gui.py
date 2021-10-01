import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from tkinter import scrolledtext
from tkinter.filedialog import askopenfilename
import os
from RC4 import *


class RC4Method:
    def encrypt(key, plaintext):
        pass

class DecryptionMethod:
    @staticmethod
    def lewat():
        pass

class UtilityFunction:
    @staticmethod
    def open_file():
        file_path = askopenfilename(filetypes=[('Files', '*')])
        if file_path is not None:
            pass
        return file_path



class ConverterFrame(ttk.Frame):
    def __init__(self, container, feature):
        super().__init__(container)

        self.feature = feature
        self.imported = False
        self.grid(column=0, row=2, padx=5, pady=5, sticky="nsew")

        if(self.feature == 'rc4'):    
            # field options
            options = {'padx': 5, 'pady': 0}

            self.inputLabel = ttk.Label(self, text='Input Text')
            self.inputLabel.grid(column=0, row=0, sticky='w', **options)
            self.inputText = tk.Text(self, height=25, width=30)
            self.inputText.grid(column=0, row=1, **options)

            self.encryptLabel = ttk.Label(self, text='Encrypted Text')
            self.encryptLabel.grid(column=1, row=0, sticky='w', **options)

            encryptFrame = tk.Frame(self, padx=25, pady=15)
            encryptFrame.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

            self.encryptText = tk.scrolledtext.ScrolledText(encryptFrame, height=25, width=30, state='disabled')
            self.encryptText.grid(column=0, row=0, **options)

            self.decryptLabel = ttk.Label(self, text='Decrypted Text')
            self.decryptLabel.grid(column=2, row=0, sticky='w', **options)
            self.decryptText = tk.Text(self, height=25, width=30, state='disabled')
            self.decryptText.grid(column=2, row=1, **options)

            # field option
            options = {'padx': 5, 'pady': 5}

            sideFrame = tk.Frame(self, padx=25, pady=15)
            sideFrame.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")

            # key1 label
            self.key1_label = ttk.Label(sideFrame, text='Key 1')
            self.key1_label.grid(column=0, row=0, sticky='n',  **options)

            # key1 entry
            self.key1 = tk.StringVar()
            self.key1_entry = ttk.Entry(sideFrame, textvariable=self.key1)
            self.key1_entry.grid(column=1, row=0, sticky='n', **options)
            self.key1_entry.focus()

            # encrypt button
            self.encrypt_button = ttk.Button(sideFrame, text='Encrypt Text')
            self.encrypt_button.grid(column=0, row=2, sticky='w', **options)
            self.encrypt_button.configure(command=self.RC4Encrypt)

            # decrypt button
            self.decrypt_button = ttk.Button(sideFrame, text='Decrypt Text')
            self.decrypt_button.grid(column=1, row=2, sticky='w', **options)
            self.decrypt_button.configure(command=self.RC4Decrypt)

        elif(self.feature == 'stegano image' or self.feature == 'stegano audio'):
            # field options
            options = {'padx': 5, 'pady': 0}

            encryptFrame = tk.Frame(self, padx=25, pady=15)
            encryptFrame.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

            self.inputFilepath = tk.Text(encryptFrame, height=1, width=30)
            self.inputFilepath.grid(column=0, row=0, **options)
            self.inputFilepath.config(state='disabled')
            
            self.importButton = ttk.Button(encryptFrame, text='Upload File')
            self.importButton.grid(column=1, row=0, sticky='w', **options)
            self.importButton.configure(command=self.importFile)

            self.inputText = tk.Text(encryptFrame, height=1, width=30)
            self.inputText.grid(column=0, row=1, **options)

            self.inputLabel = ttk.Label(encryptFrame, text='Input Text')
            self.inputLabel.grid(column=1, row=1, sticky='w', **options)

            embedFrame = tk.Frame(encryptFrame, padx=25, pady=15)
            embedFrame.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

            self.embedEncryptButton = ttk.Button(embedFrame, text='Embed with Encryption')
            self.embedEncryptButton.grid(column=0, row=0, sticky='w', **options)
            # self.embedEncryptButton.configure(command=self.importFile)

            self.embedButton = ttk.Button(embedFrame, text='Embed without Encryption')
            self.embedButton.grid(column=1, row=0, sticky='w', **options)
            # self.embedEncryptButton.configure(command=self.importFile)

            self.grid(column=0, row=2, padx=5, pady=5, sticky="nsew")
        
        elif(self.feature == 'extract image' or self.feature == 'extract audio'):
            # field options
            options = {'padx': 5, 'pady': 0}

            encryptFrame = tk.Frame(self, padx=25, pady=15)
            encryptFrame.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

            self.inputFilepath = tk.Text(encryptFrame, height=1, width=30)
            self.inputFilepath.grid(column=0, row=0, **options)
            self.inputFilepath.config(state='disabled')
            
            self.importButton = ttk.Button(encryptFrame, text='Upload File')
            self.importButton.grid(column=1, row=0, sticky='w', **options)
            self.importButton.configure(command=self.importFile)

            extractFrame = tk.Frame(encryptFrame, padx=25, pady=15)
            extractFrame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

            self.extractEncryptButton = ttk.Button(extractFrame, text='Embed with Encryption')
            self.extractEncryptButton.grid(column=0, row=0, sticky='w', **options)
            # self.embedEncryptButton.configure(command=self.importFile)

            self.extractButton = ttk.Button(extractFrame, text='Embed without Encryption')
            self.extractButton.grid(column=1, row=0, sticky='w', **options)
            # self.embedEncryptButton.configure(command=self.importFile)

            self.grid(column=0, row=2, padx=5, pady=5, sticky="nsew")
    
    def RC4Encrypt(self, event=None):
        self.encryptText.config(state='normal')
        self.encryptText.delete('1.0', 'end')
        plaintext = self.inputText.get('1.0', 'end-1c')
        input_key1 = self.key1_entry.get()
        rc4 = RC4(input_key1, plaintext)
        encryptedText = rc4.getEncryptedText()
        self.encryptText.insert(tk.INSERT, encryptedText)
        self.encryptText.config(state='disabled')

    def RC4Decrypt(self, event=None):
        self.decryptText.config(state='normal')
        self.encryptText.config(state='normal')
        encryptedText = self.encryptText.get('1.0', 'end-1c')
        plaintext = self.inputText.get('1.0', 'end-1c')
        input_key1 = self.key1_entry.get()
        rc4 = RC4(input_key1, plaintext)
        decryptedText = rc4.getDecryptedText()
        self.decryptText.insert(tk.INSERT, decryptedText)
        self.encryptText.config(state='disabled')
        self.decryptText.config(state='disabled')

    def importFile(self, event=None):
        f = UtilityFunction.open_file()
        fName, self.fileExtension = fileName, fileExtension = os.path.splitext(f)
        readFile = open(f, 'rb')
        fileReaded = readFile.read()
        b = bytearray(fileReaded)
        result = b.decode('latin-1')
        if(self.feature != "rc4"):
            self.inputFilepath.config(state='normal')
            self.inputFilepath.delete('1.0', 'end')
            self.inputFilepath.insert(tk.INSERT, fileName)
            self.inputFilepath.config(state='disabled')
        else:
            self.inputText.delete('1.0', 'end')
            self.inputText.insert(tk.INSERT, result)
            self.imported = True

    def exportFile(self, event=None):
        if(self.imported == True and self.cipherMethod == 'extended_vigenere' and self.fileExtension != '.txt'):
            exportEncrypted = 'hasilEncrypted.txt'
            save_text = open(exportEncrypted, 'w', encoding='utf-8')
            save_text.write(self.encryptedResult)
            save_text.close()

            decrypted_txt = self.decryptedResult
            b_decrypted = decrypted_txt.encode('latin-1')
            exportFileName = 'hasilDecrypted' + self.fileExtension
            save_text = open(exportFileName, 'wb')
            save_text.write(b_decrypted)
            save_text.close()
        else:
            self.encryptText.config(state='normal')
            self.encryptTextFive.config(state='normal')
            
            encrypt_txt = self.encryptText.get('1.0', 'end-1c')
            # if(self.imported == True):
            #     filename = 'hasilEncrypted' + self.fileExtension
            # else:
            filename = 'hasilEncrypted.txt'
            save_text = open(filename, 'w')
            save_text.write(encrypt_txt)
            save_text.close()

            encrypt_txt = self.encryptTextFive.get('1.0', 'end-1c')
            # if(self.imported == True):
            #     filename = 'hasilEncryptedFive' + self.fileExtension
            # else:
            filename = 'hasilEncryptedFive.txt'
            save_text = open(filename, 'w')
            save_text.write(encrypt_txt)
            save_text.close()

            self.encryptText.config(state='disabled')
            self.encryptTextFive.config(state='disabled')
        self.downloaded_label = ttk.Label(self, text='File Downloaded!')
        self.downloaded_label.grid(column=0, row=4, sticky='w')
            

    def reset(self):
        # self.key1_entry.delete(0, "end")
        # self.decryptText.config(state='normal')
        # self.encryptText.config(state='normal')
        # self.decryptText.delete('1.0', 'end')
        # self.encryptText.delete('1.0', 'end')
        # self.inputText.delete('1.0', 'end')
        # self.decryptText.config(state='disabled')
        # self.imported = False
        pass


class ControlFrame(ttk.LabelFrame):
    def __init__(self, container):

        super().__init__(container)
        self['text'] = 'Options'

        # radio buttons
        self.selected_value = tk.IntVar()

        ttk.Radiobutton(
            self,
            text='RC4',
            value=0,
            variable=self.selected_value,
            command=self.change_frame).grid(column=0, row=0, padx=5, pady=5)
        
        ttk.Radiobutton(
            self,
            text='Stegano Image',
            value=1,
            variable=self.selected_value,
            command=self.change_frame).grid(column=2, row=0, padx=5, pady=5)
        
        ttk.Radiobutton(
            self,
            text='Stegano Audio',
            value=2,
            variable=self.selected_value,
            command=self.change_frame).grid(column=3, row=0, padx=5, pady=5)
        
        ttk.Radiobutton(
            self,
            text='Extract Image',
            value=3,
            variable=self.selected_value,
            command=self.change_frame).grid(column=4, row=0, padx=5, pady=5)
        
        ttk.Radiobutton(
            self,
            text='Extract Audio',
            value=4,
            variable=self.selected_value,
            command=self.change_frame).grid(column=5, row=0, padx=5, pady=5)

        self.grid(column=0, row=1, padx=5, pady=5, sticky='ew')

        # initialize frames
        self.frames = {}
        self.frames[0] = ConverterFrame(
            container,
            'rc4')
        self.frames[1] = ConverterFrame(
            container,
            'stegano image')
        self.frames[2] = ConverterFrame(
            container,
            'stegano audio')
        self.frames[3] = ConverterFrame(
            container,
            'extract image')
        self.frames[4] = ConverterFrame(
            container,
            'extract audio')

        self.change_frame()

    def change_frame(self):
        frame = self.frames[self.selected_value.get()]
        # frame.reset()
        frame.tkraise()


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tugas 1 Kripto (13518003 | 13518116)")
        self.resizable(False, False)


if __name__ == "__main__":
    app = App()
    ControlFrame(app)
    app.mainloop()