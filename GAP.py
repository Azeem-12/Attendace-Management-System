from PIL import Image
import tkinter as tk
import numpy as np
import pandas as pd
import cv2
import csv
import os
import datetime
import time

col_dark_grey = '#262626'
col_light_grey = '#525252'
col_sky_blue = '#075985'

totalTime = 50 #seconds

def del_sc1():
    sc1.destroy()

def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry('300x100')
    sc1.iconbitmap('GAP.ico')
    sc1.title('Warning!!')
    sc1.configure(background=col_dark_grey)
    tk.Label(sc1,text='Enrollment & Name required!!!',fg=col_sky_blue,bg=col_dark_grey,font=('roboto', 16, ' bold ')).pack()
    tk.Button(sc1,text='OK',command=del_sc1,fg="white"  ,bg=col_sky_blue  ,width=9  ,height=1, activebackground = "Red" ,font=('roboto', 15, ' bold ')).place(x=90,y= 50)

def del_sc2():
    sc2.destroy()

def err_screen1():
    global sc2
    sc2 = tk.Tk()
    sc2.geometry('400x100')
    sc2.iconbitmap('GAP.ico')
    sc2.title('Warning!!')
    sc2.configure(background=col_dark_grey)
    tk.Label(sc2,text='Please enter your subject name!!!',fg=col_sky_blue,bg=col_dark_grey,font=('roboto', 16, ' bold ')).pack()
    tk.Button(sc2,text='OK',command=del_sc2,fg="white"  ,bg=col_sky_blue  ,width=9  ,height=1, activebackground = "Red" ,font=('roboto', 15, ' bold ')).place(x=150,y= 50)

def take_img():
    l1 = txt.get()
    l2 = txt2.get()
    if l1 == '':
        err_screen()
    elif l2 == '':
        err_screen()
    else:
        try:
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            Enrollment = txt.get()
            Name = txt2.get()
            count = 1
            while (True):
                _, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.2, 5)
                if len(faces) > 0:
                    (x, y, w, h) = faces[0]
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    cv2.imwrite("Faces/" + Name + "." + Enrollment + '.' + str(count-1) + ".jpg",
                                gray[y:y + h, x:x + w])
                    count += 1
                if count > 70:
                    break
                cv2.imshow('Frame', img)
                key = cv2.waitKey(10) 
                if key == ord('a'): 
                    break
            cam.release()
            cv2.destroyAllWindows()
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            row = [Enrollment, Name, Date, Time]
            with open('StudentDetails/StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile, delimiter=',')
                writer.writerow(row)
                csvFile.close()
            res = "Images Saved for Enrollment : " + Enrollment + " Name : " + Name
            Notification.configure(text=res, bg="SpringGreen3", width=50, font=('roboto', 18, 'bold'))
            Notification.place(x=250, y=400)
        except FileExistsError as F:
            f = 'Student Data already exists'
            Notification.configure(text=f, bg="Red", width=21)
            Notification.place(x=450, y=400)
        finally:
            cv2.destroyAllWindows()


def subjectchoose():
    def take_attendance():
        sub=tx.get()
        now = time.time()
        future = now + totalTime
        if time.time() < future:
            if sub == '':
                err_screen1()
            else:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read("Training/Trainner.yml")
                except:
                    e = 'Model not found,Please train model'
                    Notifica.configure(text=e, bg="red", fg="black", width=33, font=('roboto', 15, 'bold'))
                    Notifica.place(x=20, y=250)

                harcascadePath = "haarcascade_frontalface_default.xml"
                faceCascade = cv2.CascadeClassifier(harcascadePath)
                df = pd.read_csv("StudentDetails/StudentDetails.csv")
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ['Enrollment', 'Name', 'Date', 'Time']
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id
                        global Subject
                        global aa
                        global date
                        global timeStamp
                        global tt

                        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                        if (conf < 70):
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            aa = df.loc[df['Enrollment'] == Id]['Name'].values
                            if len(aa) > 0:
                                aa = aa[0]
                            else:
                                continue
                            tt = str(aa)
                            attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0), 4)

                        else:
                            Id = 'Unknown'
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)

                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                        
                    cv2.imshow('Filling attedance..', im)
                    key = cv2.waitKey(10) 
                    if key == ord('a'): 
                        break
                
                fileName = ''

                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                Hour, Minute, Second = timeStamp.split(":")
                fileName = os.getcwd() + "/Attendance/" + Subject + "_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
                attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                attendance.to_csv(fileName, index=False)

                M = 'Attendance filled Successfully'
                Notifica.configure(text=M, bg="Green", fg="white", width=33, font=('roboto', 15, 'bold'))
                Notifica.place(x=20, y=250)

                cam.release()
                cv2.destroyAllWindows()

                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background=col_dark_grey)
                with open(fileName, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            label = tkinter.Label(root, width=len(row)+1, height=1, fg=col_sky_blue, font=('mono', 15, 'bold' if r == 0 else ''), bg=col_dark_grey, text=row)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()

    windo = tk.Tk()
    windo.iconbitmap('GAP.ico')
    windo.title("Enter subject name...")
    windo.geometry('550x220')
    windo.resizable(False, False)
    windo.configure(background=col_dark_grey)
    Notifica = tk.Label(windo, text="Attendance filled Successfully", bg="Green", fg="white", width=33,
                            height=2, font=('roboto', 15, 'bold'))

    sub = tk.Label(windo, text="Enter Subject", width=15, height=2, fg=col_sky_blue, bg=col_dark_grey, font=('roboto', 20, ' bold '))
    sub.place(x=10, y=10)

    tx = tk.Entry(windo, width=25, bg=col_light_grey, fg="white", font=('roboto', 23, ''))
    tx.place(x=50, y=70)

    fill_a = tk.Button(windo, text="Take Attendance", fg="white",command=take_attendance, bg=col_sky_blue, width=20, height=2, activebackground=col_light_grey, font=('roboto', 15, ' bold '))
    fill_a.place(x=160, y=130)
    windo.mainloop()

def admin_panel():
    win = tk.Tk()
    win.iconbitmap('GAP.ico')
    win.title("Log In")
    win.geometry('700x400')
    win.resizable(False, False)
    win.configure(background=col_dark_grey)

    def log_in():
        username = un_entr.get()
        password = pw_entr.get()

        if username == 'admin' :
            if password == 'password':
                win.destroy()
                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Student Details")
                root.configure(background=col_dark_grey)

                cs = os.getcwd() + '/StudentDetails/StudentDetails.csv'
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            label = tkinter.Label(root, width=len(row)+1, height=1, fg=col_sky_blue, font=('roboto', 15, 'bold' if r == 0 else ''),bg=col_dark_grey, text=row)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
            else:
                valid = 'Incorrect ID or Password'
                Nt.configure(text=valid, bg="red", fg="black", width=38, font=('roboto', 19, 'bold'))
                Nt.place(x=120, y=350)

        else:
            valid ='Incorrect ID or Password'
            Nt.configure(text=valid, bg="red", fg="black", width=38, font=('roboto', 19, 'bold'))
            Nt.place(x=120, y=350)


    Nt = tk.Label(win, text="Attendance filled Successfully", bg="Green", fg="white", width=40,
                  height=2, font=('roboto', 19, 'bold'))

    un = tk.Label(win, text="Enter username", width=15, height=2, fg=col_sky_blue, bg=col_dark_grey,
                   font=('roboto', 15, ' bold '))
    un.place(x=30, y=50)

    pw = tk.Label(win, text="Enter password", width=15, height=2, fg=col_sky_blue, bg=col_dark_grey,
                  font=('roboto', 15, ' bold '))
    pw.place(x=30, y=150)

    un_entr = tk.Entry(win, width=20, bg=col_light_grey, fg="white", font=('roboto', 20, ''))
    un_entr.place(x=290, y=55)

    pw_entr = tk.Entry(win, width=20,show="*", bg=col_light_grey, fg="white", font=('roboto', 20, ''))
    pw_entr.place(x=290, y=155)

    Login = tk.Button(win, text="Log In", fg="white", bg=col_sky_blue, width=20,
                       height=2,
                       activebackground=col_light_grey,command=log_in, font=('roboto', 15, ' bold '))
    Login.place(x=290, y=250)
    win.mainloop()

def trainimg():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    global detector
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    try:
        global faces,Id
        faces, Id = getImagesAndLabels("Faces")
    except Exception as e:
        l='please make "Faces" folder & put Images'
        Notification.configure(text=l, bg="SpringGreen3", width=50, font=('roboto', 18, 'bold'))
        Notification.place(x=350, y=400)

    recognizer.train(faces, np.array(Id))
    try:
        recognizer.save("Training/Trainner.yml")
    except Exception as e:
        q='Please make "Training" folder'
        Notification.configure(text=q, bg="SpringGreen3", width=50, font=('roboto', 18, 'bold'))
        Notification.place(x=350, y=400)

    res = "Model Trained"
    Notification.configure(text=res, bg="SpringGreen3", width=50, font=('roboto', 18, 'bold'))
    Notification.place(x=250, y=400)

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')

        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(imageNp)
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)
    return faceSamples, Ids


def on_closing():
    from tkinter import messagebox
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()

window = tk.Tk()
window.title("Galgotias Attendance Portal")

window.geometry('1280x720')
window.resizable(False,False)
window.configure(background=col_dark_grey)
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.iconbitmap('GAP.ico')
window.protocol("WM_DELETE_WINDOW", on_closing)

message = tk.Label(window, text="Galgotias Attendance Portal", bg=col_light_grey, fg=col_dark_grey, width=35, height=1, font=('roboto', 40, 'bold'))

message.place(x=80, y=20)

Notification = tk.Label(window, text="All things good", bg="Green", fg="white", width=15,
                      height=3, font=('roboto', 17, 'bold'))

lbl = tk.Label(window, text="Enter Enrollment", width=20, height=1, bg = col_dark_grey, fg=col_sky_blue, font=('roboto', 25, ' bold '))
lbl.place(x=200, y=200)

def testVal(inStr,acttyp):
    if acttyp == '1':
        if not inStr.isdigit():
            return False
    return True

txt = tk.Entry(window, validate="key", width=30, bg=col_light_grey, fg="white", font=('roboto', 20, ''))
txt['validatecommand'] = (txt.register(testVal),'%P','%d')
txt.place(x=550, y=210)

lbl2 = tk.Label(window, text="Enter Name", width=20, bg=col_dark_grey, fg=col_sky_blue, height=1, font=('roboto', 25, ' bold '))
lbl2.place(x=200, y=300)

txt2 = tk.Entry(window, width=30, bg=col_light_grey, fg="white", font=('roboto', 20, ''))
txt2.place(x=550, y=310)

takeImg = tk.Button(window, text="Take Images",command=take_img,fg="white"  ,bg=col_sky_blue  ,width=20  ,height=3, activebackground = col_light_grey ,font=('roboto', 15, ' bold '))
takeImg.place(x=90, y=500)

trainImg = tk.Button(window, text="Train Images",fg="white",command=trainimg ,bg=col_sky_blue  ,width=20  ,height=3, activebackground = col_light_grey ,font=('roboto', 15, ' bold '))
trainImg.place(x=380, y=500)

FA = tk.Button(window, text="Automatic Attendace",fg="white",command=subjectchoose  ,bg=col_sky_blue  ,width=20  ,height=3, activebackground = col_light_grey ,font=('roboto', 15, ' bold '))
FA.place(x=670, y=500)

AP = tk.Button(window, text="Check Register students",command=admin_panel,fg="white"  ,bg=col_sky_blue  ,width=20 ,height=3, activebackground = col_light_grey ,font=('roboto', 15, ' bold '))
AP.place(x=960, y=500)

window.mainloop()