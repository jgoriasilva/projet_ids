import cv2, time, smtplib, csv
from random import randint
import sys 
import select
import tkinter as tk
from tkinter import ttk

#Get list of worker IDs from database
with open("info_employes.txt", "r") as f:
    reader = csv.DictReader(f)
    employee_info = list(reader)
    
exp = ""


#######################################################################
###                            GUI                                  ###
#######################################################################
useqr = True

#GUI for intro message
def gui(msg, name):
    if (msg == 1):
        root = tk.Tk()
        root.title('GUI')
        def bp():
            global useqr
            useqr = False
            root.destroy() 
        message0 = tk.Label(text = " \n \n \n \n \n ")
        message0.pack()
        message1 = tk.Label(text = "Veuillez vous identifier \n")
        message1.pack()
        message1.config(font=("Courier", 20))
        message2 = tk.Label(text = "Présentez votre carte d'identité d'employé \n avec son code QR \n")
        message2.pack()
        message2.config(font=("Courier", 20))
        message3 = tk.Label(text = "Ou appuyez le button pour saisir \n manuellement votre  numéro d'employé \n")
        message3.pack()
        message3.config(font=("Courier", 20))    
        btn3 = ttk.Button(root,text = 'SAISIR MANUELLEMENT' , width = 30, command = lambda : bp())
        btn3.pack()
        label = tk.Label(root, font = ("Courier", 30))
        label.place(x=380, y=15)
        def countdown(count):
            label['text'] = count
        root.attributes("-fullscreen",True)
        root.after(15000, root.destroy)
        root.after(0, countdown, 15)
        root.after(1000, countdown, 14)
        root.after(2000, countdown, 13)
        root.after(3000, countdown, 12)
        root.after(4000, countdown, 11)
        root.after(5000, countdown, 10)
        root.after(6000, countdown, 9)
        root.after(7000, countdown, 8)
        root.after(8000, countdown, 7)
        root.after(9000, countdown, 6)
        root.after(10000, countdown, 5)
        root.after(11000, countdown, 4)
        root.after(12000, countdown, 3)
        root.after(13000, countdown, 2)
        root.after(14000, countdown, 1)
        root.mainloop()   
        return useqr        
    elif (msg == 2):
        root = tk.Tk()
        root.title('GUI')
        message0 = tk.Label(text = " \n \n \n \n \n \n ")
        message0.pack()
        message1 = tk.Label(text = "Impossible à identifier : \n essayez à nouveau")
        message1.pack()
        message1.config(font=("Courier", 20))
        root.attributes("-fullscreen",True)
        root.after(5000, root.destroy)
        root.mainloop()
        return
    elif(msg == 3):
        root = tk.Tk()
        root.title('GUI')
        message0 = tk.Label(text = " \n \n \n \n \n \n ")
        message0.pack()
        message1 = tk.Label(text = "Impossible à identifier via le code QR")
        message1.pack()
        message1.config(font=("Courier", 20))
        root.attributes("-fullscreen",True)
        root.after(5000, root.destroy)
        root.mainloop()
        return
    elif(msg == 4):
        root = tk.Tk()
        root.title('GUI')
        message0 = tk.Label(text = " \n \n \n \n \n \n ")
        message0.pack()
        message1 = tk.Label(text = "Le numéro d'identité n'a pas été identifiée. \n Veuillez réessayer.")
        message1.pack()
        message1.config(font=("Courier", 20))
        root.attributes("-fullscreen",True)
        root.after(5000, root.destroy)
        root.mainloop()
        return
    elif(msg == 5):
        root = tk.Tk()
        root.title('GUI')
        message0 = tk.Label(text = " \n \n \n \n \n \n ")
        message0.pack()
        sttt = "Bienvenue : " + name
        message1 = tk.Label(text = sttt)
        message1.pack()
        message1.config(font=("Courier", 20))
        message2 = tk.Label(text = "\n \n Un courriel a été envoyé à \n l'adresse électronique de votre entreprise \n avec un mot de passe")
        message2.pack()
        message2.config(font=("Courier", 20))
        root.attributes("-fullscreen",True)
        root.after(5000, root.destroy)
        root.mainloop()
        return        
    elif(msg == 6):
        root = tk.Tk()
        root.title('GUI')
        message0 = tk.Label(text = " \n \n \n \n \n \n ")
        message0.pack()
        message1 = tk.Label(text = "MAUVAIS MOT DE PASSE \n \n ESSAYEZ À NOUVEAU")
        message1.pack()
        message1.config(font=("Courier", 20))
        root.attributes("-fullscreen",True)
        root.after(3000, root.destroy)
        root.mainloop()
        return
    elif(msg == 7):
        root = tk.Tk()
        root.title('GUI')
        root.configure(bg='green')
        message0 = tk.Label(text = " \n \n \n \n \n \n \n \n \n \n \n \n ", bg = "green")
        message0.pack()
        message1 = tk.Label(text = "VÉRIFIÉ", bg = "green", fg = 'white')
        message1.pack()
        message1.config(font=("Courier", 20))
        root.attributes("-fullscreen",True)
        root.after(5000, root.destroy)
        root.mainloop()
        return
    elif(msg == 8):
        root = tk.Tk()
        root.title('GUI')
        root.configure(bg='red')
        message0 = tk.Label(text = " \n \n \n \n \n \n \n \n \n \n \n \n ", bg = "red")
        message0.pack()
        message1 = tk.Label(text = "ALARM!", bg = "red", fg = 'white')
        message1.pack()
        message1.config(font=("Courier", 20))
        root.attributes("-fullscreen",True)
        root.after(5000, root.destroy)
        root.mainloop()
        return  


########################################################################
###                              FUNCTIONS                           ###
######################################################################## 

#QR Scanner Raspberry Pi camera
def qrscanner():
    
    start_time = time.time() #Start time of program to detect when th robot starts asking for the ID        
    
    # set up camera object
    cap = cv2.VideoCapture(0)

    # QR code detection object
    detector = cv2.QRCodeDetector()

    while True:
        # get the image
        _, img = cap.read()
        # get bounding box coords and data
        data, bbox, _ = detector.detectAndDecode(img)
        
        #NEW WINDOW TO MAKE IT FULLSCREEN
        cv2.namedWindow('screen',cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('screen',cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        # if there is a bounding box, draw one, along with the data
        if(bbox is not None):
            for i in range(len(bbox)):
                cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
                         0, 255), thickness=2)
            cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
            #display data
            if data:
                #print("data found: ", data)
                #detect if identifies the ID
                cap.release()
                cv2.destroyAllWindows()
                return data
                    
            
        # display the image preview
        cv2.imshow('screen', img)
        
        #if employee has no ID he can demand to input it
        if(cv2.waitKey(1) == ord("q")): 
        # free camera object and exit if button pressed
            cap.release()
            cv2.destroyAllWindows()
            return("ManuallyInputID")
        
        if (time.time() - start_time  > 10):
            cap.release()
            cv2.destroyAllWindows()
            return("none")
            



#def demandID_time():
#     print("Veuillez saisir votre numéro d'identification d'employé")
# 
#     i, o, e = select.select( [sys.stdin], [], [], 10)
# 
#     if (i):
#         thing = sys.stdin.readline().strip()
#         return thing
#     else:
#         return("none")

def demandID():
    key = tk.Tk()  # key window name
    key.title('INSERT ID NUMBER')  # title Name

    # exp = ""          # global variable 
    # showing all data in display
    
    def press(num):
        global exp
        exp=exp + str(num)
        equation.set(exp)

    def clear():
        global exp
        exp = ""
        equation.set(exp)

    def Tab():
      exp = " TAB : "
      equation.set(exp)
      
    # text
    msg0 = tk.Label(key, text="").grid(row=0, column=0, ipadx = 25, ipady = 5)
    msg1 = tk.Label(key, text="").grid(row=0, column=1, ipadx = 25, ipady = 5)
    msg2 = tk.Label(key, text="").grid(row=0, column=2, ipadx = 25, ipady = 5)

    message0 = tk.Label(key, text="ÉCRIVEZ VOTRE IDENTIFIANT D'EMPLOYÉ").grid(row=1, column=3, columnspan = 5)

    # entry box
    equation = tk.StringVar()
    Dis_entry = ttk.Entry(key,state= 'readonly',textvariable = equation)
    Dis_entry.grid(column = 3, row = 2, rowspan= 1 , columnspan = 3, ipadx = 0)


    # add all button line wise 

    # First Line Button

    btn1 = ttk.Button(key,text = '1' , width = 10, command = lambda : press('1'))
    btn1.grid(row = 3 , column = 3, ipadx = 30 , ipady = 35)

    btn2 = ttk.Button(key,text = '2' , width = 10, command = lambda : press('2'))
    btn2.grid(row = 3 , column = 4, ipadx = 30 , ipady = 35)

    btn3 = ttk.Button(key,text = '3' , width = 10, command = lambda : press('3'))
    btn3.grid(row = 3 , column = 5, ipadx = 30 , ipady = 35)



    # Second Line Button

    btn4 = ttk.Button(key,text = '4' , width = 10, command = lambda : press('4'))
    btn4.grid(row = 4 , column = 3, ipadx = 30 , ipady = 35)

    btn5 = ttk.Button(key,text = '5' , width = 10, command = lambda : press('5'))
    btn5.grid(row = 4 , column = 4, ipadx = 30 , ipady = 35)

    btn6 = ttk.Button(key,text = '6' , width = 10, command = lambda : press('6'))
    btn6.grid(row = 4 , column = 5, ipadx = 30 , ipady = 35)

    # third line Button

    btn7 = ttk.Button(key,text = '7' , width = 10, command = lambda : press('7'))
    btn7.grid(row = 5 , column = 3, ipadx = 30 , ipady = 35)

    btn8 = ttk.Button(key,text = '8' , width = 10, command = lambda : press('8'))
    btn8.grid(row = 5 , column = 4, ipadx = 30 , ipady = 35)

    btn9 = ttk.Button(key,text = '9' , width = 10, command = lambda : press('9'))
    btn9.grid(row = 5 , column = 5, ipadx = 30 , ipady = 35)

    #Fourth Line Button

    clear = ttk.Button(key,text = 'Clear' , width = 10, command = clear)
    clear.grid(row = 6 , column = 3, ipadx = 30 , ipady = 35)

    btn0 = ttk.Button(key,text = '0' , width = 10, command = lambda : press('0'))
    btn0.grid(row = 6 , column = 4, ipadx = 30 , ipady = 35)

    enter = ttk.Button(key,text = 'Enter' , width = 10, command = key.destroy)
    enter.grid(row = 6 , column = 5, ipadx = 30 , ipady = 35)
    
    #After a given ammount of time, end the screen
    key.after(15000, key.destroy) 

    key.attributes("-fullscreen",True)

    key.mainloop()  # using ending point
    
    return exp
 
def send_email(sendTo,password):
         #Email Variables
    SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
    SMTP_PORT = 587 #Server Port (don't change!)
    GMAIL_USERNAME = 'fausseentrepriseids@gmail.com' #change this to match your gmail account
    GMAIL_PASSWORD = 'raspberry12345pi'  #change this to match your gmail password
     
    class Emailer:
        def sendmail(self, recipient, subject, content):
             
            #Create Headers
            headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient,
                       "MIME-Version: 1.0", "Content-Type: text/html"]
            headers = "\r\n".join(headers)
     
            #Connect to Gmail Server
            session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            session.ehlo()
            session.starttls()
            session.ehlo()
     
            #Login to Gmail
            session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
     
            #Send Email & Exit
            session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
            session.quit
     
    sender = Emailer()
     
    #sendTo = 'federicogarciavlz@gmail.com'
    emailSubject = "MOT DE PASSE"
    emailContent = str(password)
     
    #Sends an email to the "sendTo" address with the specified "emailSubject" as the subject and "emailContent" as the email content.
    sender.sendmail(sendTo, emailSubject, emailContent)  


def demandPassword(password):
    key = tk.Tk()  # key window name
    key.title('INSERT PASSWORD')  # title Name

    # exp = ""          # global variable 
    # showing all data in display
    
    def press(num):
        global exp
        exp=exp + str(num)
        equation.set(exp)

    def clear():
        global exp
        exp = ""
        equation.set(exp)

    def Tab():
      exp = " TAB : "
      equation.set(exp)
      
    # text
    msg0 = tk.Label(key, text="").grid(row=0, column=0, ipadx = 25, ipady = 5)
    msg1 = tk.Label(key, text="").grid(row=0, column=1, ipadx = 25, ipady = 5)
    msg2 = tk.Label(key, text="").grid(row=0, column=2, ipadx = 25, ipady = 5)

    message0 = tk.Label(key, text="ÉCRIVEZ LE MOT DE PASSE").grid(row=1, column=3, columnspan = 5)

    # entry box
    equation = tk.StringVar()
    Dis_entry = ttk.Entry(key,state= 'readonly',textvariable = equation)
    Dis_entry.grid(column = 3, row = 2, rowspan= 1 , columnspan = 3, ipadx = 0)


    # add all button line wise 

    # First Line Button

    btn1 = ttk.Button(key,text = '1' , width = 10, command = lambda : press('1'))
    btn1.grid(row = 3 , column = 3, ipadx = 30 , ipady = 35)

    btn2 = ttk.Button(key,text = '2' , width = 10, command = lambda : press('2'))
    btn2.grid(row = 3 , column = 4, ipadx = 30 , ipady = 35)

    btn3 = ttk.Button(key,text = '3' , width = 10, command = lambda : press('3'))
    btn3.grid(row = 3 , column = 5, ipadx = 30 , ipady = 35)



    # Second Line Button

    btn4 = ttk.Button(key,text = '4' , width = 10, command = lambda : press('4'))
    btn4.grid(row = 4 , column = 3, ipadx = 30 , ipady = 35)

    btn5 = ttk.Button(key,text = '5' , width = 10, command = lambda : press('5'))
    btn5.grid(row = 4 , column = 4, ipadx = 30 , ipady = 35)

    btn6 = ttk.Button(key,text = '6' , width = 10, command = lambda : press('6'))
    btn6.grid(row = 4 , column = 5, ipadx = 30 , ipady = 35)

    # third line Button

    btn7 = ttk.Button(key,text = '7' , width = 10, command = lambda : press('7'))
    btn7.grid(row = 5 , column = 3, ipadx = 30 , ipady = 35)

    btn8 = ttk.Button(key,text = '8' , width = 10, command = lambda : press('8'))
    btn8.grid(row = 5 , column = 4, ipadx = 30 , ipady = 35)

    btn9 = ttk.Button(key,text = '9' , width = 10, command = lambda : press('9'))
    btn9.grid(row = 5 , column = 5, ipadx = 30 , ipady = 35)

    #Fourth Line Button

    clear = ttk.Button(key,text = 'Clear' , width = 10, command = clear)
    clear.grid(row = 6 , column = 3, ipadx = 30 , ipady = 35)

    btn0 = ttk.Button(key,text = '0' , width = 10, command = lambda : press('0'))
    btn0.grid(row = 6 , column = 4, ipadx = 30 , ipady = 35)

    enter = ttk.Button(key,text = 'Enter' , width = 10, command = key.destroy)
    enter.grid(row = 6 , column = 5, ipadx = 30 , ipady = 35)
    
    #After a given ammount of time, end the screen
    key.after(15000, key.destroy) 

    key.attributes("-fullscreen",True)

    key.mainloop()  # using ending point
    
    checkPassword = False
    
    if (str(exp) == str(password)):
        checkPassword = True
    
    return checkPassword
    
    return exp

def checkID(data):
    foundID = False
    #print("Data:",data)
    found_values = []
    for dictionary in employee_info:
        if (dictionary["id number"] == data):
            found_values.append(dictionary)
            name = found_values[0].get('name')
            email = found_values[0].get('email')
            #print("A comfirmation password has been sent to your email")
            foundID = True
    if (foundID):
        return foundID, name, email
    else:
        return foundID, None, None

def alarm():
    #security function
    #alert all systems
    gui(8, "")


#######################################################################
###                             MAIN                                ###
#######################################################################

#QR CODE READER (TRY 1)
useqr = gui(1, "")

if (useqr):
    dataQR = qrscanner() #Start the program by demainding the QR Code to the identified person
    identified, _, _ = checkID(dataQR)

    if (dataQR != "ManuallyInputID"): #only enter here if the button for pressing ID wasn't pushed (give 3 attempts for QR scanner)
        #QR CODE READER (TRY 2)
        if (identified == False):
            gui(2, "")
            dataQR = qrscanner() #Demaind the QR Code again (3 tries)
            identified, _, _ = checkID(dataQR)
        if (dataQR != "ManuallyInputID"):
            #QR CODE READER (TRY 3)
            if (identified == False):
                gui(2, "")
                dataQR = qrscanner() #Demaind the QR Code again (3 tries)
                identified, _, _ = checkID(dataQR)
else:
    identified = False
    
    
#IF ID NOT VERIFIED VIA QR, DEMAND ID MANUALLY    
if (identified == False):
    gui(3, "")
    exp = ""
    id_number = demandID()
    identified, _, _ = checkID(str(id_number))
    
    #IF AFTER 10S NOT VERIFIED OR ERRONEUS ID, ASK AGAIN
    if (identified == False or id_number == "none"):
        gui(4, "")
        exp = ""
        id_number = demandID()
        identified, _, _ = checkID(str(id_number))
    
    #IF STILL NOT VERIFIABLE, SOUND THE ALARM. IF THE ID IS FOUND, SEND AN EMAIL WITH PASSWORD
    if (identified == False or id_number == "none"):
        alarm()
    else: #IF ID FOUND, SEND EMAIL TO RESPECTIVE EMPLOYEE WITH PASSWORD (2-STEP VERIFICATION)
        _, name, email = checkID(str(id_number))
        password = randint(100000,999999)
        send_email(email,password)
        gui(5, name)
        exp = ""
        identified = demandPassword(password)
        
        #IF PASSWORD INPUTED INCORRECTLY, GIVE ANOTHER TRY
        if (identified == False):
            gui(6, "")
            exp = ""
            identified = demandPassword(password)
        
        #IF PASSWORD INPUTED INCORRECTLY A SECOND TIME, SOUND THE ALARM
        if (identified == False):
            alarm()
        else: #IF PASSWORD INPUTED CORRECTLY, ALLOW TO CONTINUE
            gui(7, "")
else:
    gui(7, "")
    


