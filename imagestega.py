from tkinter import *
from PIL import Image, ImageTk
from tkinter import Tk, filedialog, Button, Label
import cv2
import numpy as np
import math


def UploadImage():
	global path
	path = filedialog.askopenfilename()
	load_image = Image.open(path)
	size_image = 300,300
	load_image.thumbnail(size_image, Image.ANTIALIAS)
	render = ImageTk.PhotoImage(load_image)
	img = Label(root, image=render)
	img.image = render
	img.place(x=20, y=50)

def EncryptSeqImage():
    global path
    message = input_text.get(1.0, "end-1c")
    # print("masuk message : ",message)
    img = cv2.imread(path)
    message = [format(ord(i), '08b') for i in message]
    print(img.shape)
    # print(len(message))
    # print(message)

    _, width, _ = img.shape
    total_pixel = len(message) * 3
    total_row = math.ceil(total_pixel/width)

    count = 0
    count_char = 0
    p = 0
    for i in range(total_row + 1):
        while(count < width and count_char < len(message)):
            char = message[count_char]
            print('char :', chr(int(''.join(char), 2)))
            print('bin char', char)
            count_char += 1
            for cx, c in enumerate(char):
                print("-----", cx, "------")
                print("before change",img[i][count][cx%3])
                if((c == '0' and img[i][count][cx%3] % 2 == 1)):
                    img[i][count][cx % 3] += 1
                elif(c == '1' and img[i][count][cx%3] % 2 == 0):
                    img[i][count][cx % 3] += 1
                print("after change",img[i][count][cx%3])
                if(cx % 3 == 2):
                    count += 1
                if(cx == 7):
                    print("EOF before change",img[i][count][2])
                    if((count_char * 3 < total_pixel) and (img[i][count][2] % 2 == 1)):
                        print("masuk endline")
                        img[i][count][2] += 1
                    if ((count_char * 3 >= total_pixel) and (img[i][count][2] % 2 == 0)):
                        #end of file
                        print("masuk endFILE")
                        img[i][count][2] += 1
                    print("EOF after change",img[i][count][2])
                    count+=1
        count = 0
    cv2.imwrite("hidden_msg_img.png", img)
    success_label = Label(root, text="Encryption Successful!",highlightbackground="#3E4149")
    success_label.place(x=160, y=410)

def DecryptSeqImage():
    global path

    img = cv2.imread(path)
    message = []
    is_eof = False
    for _, arr_i in enumerate(img):
        # print(type(i))
        arr_i.tolist()
        # print(i,arr_i)
        for j, arr_j in enumerate(arr_i):
            if(j%3 == 2):
                message.append(bin(arr_j[0])[-1])
                message.append(bin(arr_j[1])[-1])
                if(bin(arr_j[2])[-1] == '1'):
                    is_eof = True
                    break
            else:
                message.append(bin(arr_j[0])[-1])
                message.append(bin(arr_j[1])[-1])
                message.append(bin(arr_j[2])[-1])
        if(is_eof):
            break
    result =[]
    k = 0
    print(len(message))
    while(k<len(message)):
        # print("k",k)
        char = []
        for i in range(k,k+8):
            # print("i",i)
            char.append(message[i])
        # print("ini char ke -",k, char)
        result.append(chr(int(''.join(char), 2)))
        k+=8
    result = ''.join(result)
    print(result)
    result_label = Label(root, text = result, highlightbackground="#3E4149")
    result_label.place(x=160, y=460)


root = Tk()
root.configure(background='grey')
root.title("Steganography")
root.geometry("600x600")

upload_button = Button(root, text="Choose Image", highlightbackground="#3E4149", command=UploadImage)
upload_button.place(x= 350, y=50)

input_text = Text(root, wrap=WORD)
input_text.place(x=20, y = 350, height = 50, width=350)

encode_button = Button(root, text="Encode", highlightbackground="#3E4149", command=EncryptSeqImage)
encode_button.place(x = 400, y = 360)
decode_button = Button(root, text="Decode", highlightbackground="#3E4149", command=DecryptSeqImage)
decode_button.place(x = 400, y = 460)


root.mainloop()