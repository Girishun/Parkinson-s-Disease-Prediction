import tensorflow as tf
import glob
import random
from keras_preprocessing.image import ImageDataGenerator
from keras_preprocessing import image
import numpy as np
import shutil
import easygui
from keras.models import load_model
import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import sqlite3


UPLOAD_FOLDER='uploads/all_class'
IMAGE_SIZE=64
my_w = tk.Tk()
my_w.geometry('1020x710+0+10')  
my_w.title('Parkinsons Disease Predictor')
my_font1=('times', 18, 'bold')

bg = PhotoImage(file='backgroundpic1.png')
bgLabel = Label(my_w, image=bg)
bgLabel.place(x=0, y=0)
my_w.grid_rowconfigure(0, weight=1)
my_w.grid_columnconfigure(0, weight=1)

message = tk.Label(my_w, text="Parkinson disease prediction" ,bg="black" , fg="cyan3"  ,font=('times', 30, 'bold'))

message.place(x=5, y=5)


#=======================================VARIABLES=====================================
USERNAME = StringVar()
PASSWORD = StringVar()
FIRSTNAME = StringVar()
LASTNAME = StringVar()

#=======================================METHODS=======================================

def Database():
    global conn, cursor
    conn = sqlite3.connect("db_member.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT, firstname TEXT, lastname TEXT)")


def Exit():
    result = tkMessageBox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        my_w.destroy()
        exit()



def LoginForm():
    global LoginFrame, lbl_result1
    LoginFrame = Frame(my_w,bg="black")
    LoginFrame.place(x=250,y=230)
    #LoginFrame.pack(side=TOP, pady=100)
    lbl_username = Label(LoginFrame, text="Username:", font=('arial', 23), bd=18,bg="black",fg="cyan3")
    lbl_username.grid(row=1)
    lbl_password = Label(LoginFrame, text="Password:", font=('arial', 23), bd=18,bg="black",fg="cyan3")
    lbl_password.grid(row=2)
    lbl_result1 = Label(LoginFrame, text="", font=('arial', 18),bg="black",fg="cyan3")
    lbl_result1.grid(row=3, columnspan=2)
    username = Entry(LoginFrame, font=('arial', 20), textvariable=USERNAME, width=17)
    username.grid(row=1, column=1)
    password = Entry(LoginFrame, font=('arial', 20), textvariable=PASSWORD, width=17, show="*")
    password.grid(row=2, column=1)
    btn_login = Button(LoginFrame, text="Login", font=('arial', 18), width=26, command=Login,bg="cyan3",fg="black")
    btn_login.grid(row=4, columnspan=2, pady=20)
    lbl_register = Label(LoginFrame, text="Register", font=('arial', 17),bg="cyan3",fg="black")
    lbl_register.grid(row=0, sticky=W)
    lbl_register.bind('<Button-1>', ToggleToRegister)
    


def RegisterForm():
    global RegisterFrame, lbl_result2
    RegisterFrame = Frame(my_w,bg="black")
    RegisterFrame.place(x=250,y=230)
    #RegisterFrame.pack(side=TOP, pady=40)
    lbl_username = Label(RegisterFrame, text="Username:", font=('arial', 18), bd=18,bg="black",fg="cyan3")
    lbl_username.grid(row=1)
    lbl_password = Label(RegisterFrame, text="Password:", font=('arial', 18), bd=18,bg="black",fg="cyan3")
    lbl_password.grid(row=2)
    lbl_firstname = Label(RegisterFrame, text="Firstname:", font=('arial', 18), bd=18,bg="black",fg="cyan3")
    lbl_firstname.grid(row=3)
    lbl_lastname = Label(RegisterFrame, text="Lastname:", font=('arial', 18), bd=18,bg="black",fg="cyan3")
    lbl_lastname.grid(row=4)
    lbl_result2 = Label(RegisterFrame, text="", font=('arial', 18))
    lbl_result2.grid(row=5, columnspan=2)
    username = Entry(RegisterFrame, font=('arial', 20), textvariable=USERNAME, width=20)
    username.grid(row=1, column=1)
    password = Entry(RegisterFrame, font=('arial', 20), textvariable=PASSWORD, width=20, show="*")
    password.grid(row=2, column=1)
    firstname = Entry(RegisterFrame, font=('arial', 20), textvariable=FIRSTNAME, width=20)
    firstname.grid(row=3, column=1)
    lastname = Entry(RegisterFrame, font=('arial', 20), textvariable=LASTNAME, width=20)
    lastname.grid(row=4, column=1)
    btn_login = Button(RegisterFrame, text="Register", font=('arial', 18), width=25, command=Register,bg="cyan3",fg="black")
    btn_login.grid(row=6, columnspan=2, pady=20)
    lbl_login = Label(RegisterFrame, text="Login",  font=('arial', 17),bg="cyan3",fg="black")
    lbl_login.grid(row=0, sticky=W)
    lbl_login.bind('<Button-1>', ToggleToLogin)

def ToggleToLogin(event=None):
    RegisterFrame.destroy()
    LoginForm()

def ToggleToRegister(event=None):
    LoginFrame.destroy()
    RegisterForm()

def Register():
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "" or FIRSTNAME.get() == "" or LASTNAME.get == "":
        lbl_result2.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ?", (USERNAME.get(),))
        if cursor.fetchone() is not None:
            lbl_result2.config(text="Username is already taken", fg="red")
        else:
            cursor.execute("INSERT INTO `member` (username, password, firstname, lastname) VALUES(?, ?, ?, ?)", (str(USERNAME.get()), str(PASSWORD.get()), str(FIRSTNAME.get()), str(LASTNAME.get())))
            conn.commit()
            USERNAME.set("")
            PASSWORD.set("")
            FIRSTNAME.set("")
            LASTNAME.set("")
            lbl_result2.config(text="Successfully Created!", fg="black")
        cursor.close()
        conn.close()

def Login():
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result1.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? and `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            lbl_result1.config(text="You Successfully Login", fg="blue")
            LoginFrame.destroy()
            park()
        else:
            lbl_result1.config(text="Invalid Username or password", fg="red")

LoginForm()
menubar = Menu(my_w)



def park():

   def load_and_preprocess_image():
      test_fldr='uploads'
      test_generator=ImageDataGenerator(rescale=1./255).flow_from_directory(
         test_fldr,
         target_size = (IMAGE_SIZE, IMAGE_SIZE),
         batch_size = 1,
         class_mode = None,
         shuffle = False)
      test_generator.reset()
      return test_generator

   def classify(model):
      batch_size = 1
      test_generator = load_and_preprocess_image()
      prob = model.predict_generator(test_generator, steps=len(test_generator)/batch_size)
      classified_prob = prob[0][0] if prob[0][0] >= 0.5 else 1 - prob[0][0]

      return classified_prob

   def logout():
       my_w.destroy()

        

   
   l1 = tk.Label(my_w,text='UPLOAD FILES & GET RESULTS',width=30,font=my_font1,bg='black',
                      fg='yellow',)  
   l1.place(x=350, y=130, width=380)
   b1 = tk.Button(my_w, text='UPLOAD IMAGES',width=20,command = lambda:result(), activebackground='skyblue',font=('bold',17) ,bg='black',fg='yellow')
   b1.place(x=385,y=450, width=240, height=40)
   print(tf.__version__)

   titleLabel = Label(my_w, text='PARKINSONS DISEASE PREDICTION SYSTEM ', font=('italic', 25, 'bold '), bg='black',
                      fg='DarkTurquoise', )
   titleLabel.place(x=0, y=10,width=1100, height=80)


   b1 = tk.Button(my_w, text='Exit',command = lambda:logout(), activebackground='skyblue',font=('bold',17) ,bg='black',fg='yellow')
   b1.place(x=930,y=32)

   model1 = load_model('model/Class1/model_Class1.h5',compile=False)
   model2 = load_model('model/Class2/model_Class2.h5',compile=False)
   model3 = load_model('model/Class3/model_Class3.h5',compile=False)


   def result():
      filelist=glob.glob('uploads/all_class/*.*')
      for filePath in filelist:
         try:
            os.remove(filePath)
         except:
            print("Error While Deleting File")
      filename =upload_file()
      test_image2 = image.load_img(filename, target_size = (64, 64))
      test_image2 = image.img_to_array(test_image2)
      test_image2 = np.expand_dims(test_image2, axis = 0)   
      result1 = model1.predict(test_image2)
      print(result1)
      result2 = model2.predict(test_image2)
      print(result2)
      result3 = model3.predict(test_image2)
      print(result3)

      if result1[0][0] == 1:
         if result2[0][0] == 1:
            if  result3[0][0] == 1:
               prediction2='Parkinsons predicted'
               value="Drug-Induced Parkinson"
            else:
               prediction2='Parkinsons predicted'
               value="Vascular Parkinson"
         else:
            prediction2='Parkinsons predicted'
            value="Idiopathic Parkinson"
      else:
         prediction2 = 'Normal'
         value="Normal"
      print(prediction2,value)
      prediction=prediction2
      values=value
      l2 = tk.Label(my_w,text="Result :  "+prediction,width=30,font=my_font1,bg='black',
                      fg='DarkTurquoise',)  
      l2.place(x=115, y=500, width=400,height=55)
      l3 = tk.Label(my_w,text="Type  :  "+values,width=30,font=my_font1,bg='black',
                      fg='DarkTurquoise',)  
      l3.place(x=475, y=560, width=440,height=55)
      shutil.copy(filename,UPLOAD_FOLDER)
      prob=classify(model1)

      l4 = tk.Label(my_w,text="Accuracy :  "+str(prob),width=30,font=my_font1,bg='black',
                      fg='DarkTurquoise',)  
      l4.place(x=115, y=620, width=400,height=55)
      return filename


          
   def upload_file():
      filename=easygui.fileopenbox()
      print(filename)
      img=Image.open(filename)
      img=img.resize((200,140))
      img=ImageTk.PhotoImage(img)
      e1 =tk.Label(my_w)
      e1.place(x=380, y=180, width=240, height=250)
      e1.image = img
      e1['image']=img
      return filename


my_w.mainloop()




