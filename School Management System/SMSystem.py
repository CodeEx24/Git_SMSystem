#from cmath import exp
#from re import sub
#from multiprocessing import Array
#from operator import truediv
#from curses.ascii import isdigit
from tkinter import *
from tkinter import ttk
import tkinter as tk
from turtle import bgcolor
from PIL import Image, ImageTk #pip install pillow
import pymysql #pip install pymysql
from tkinter import messagebox
import customtkinter as ctk
import keyboard #pip install keyboard command.

#placeholders for entry
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

#Graphical User Interface
root = ctk.CTk()
root.title("School Management System")
root.geometry("1280x720")
photo = PhotoImage(file = "PUPLogo.png") #Changes the icon logo
root.iconphoto(False, photo)
root.resizable(False,False)

def connection():
    conn=pymysql.connect(host='localhost', user='root', password='', db='school_db')
    return conn

#Tabs for each table
nbTab = ttk.Notebook(root)
nbTab.pack()

#######################################################################################################
#GENERAL VALIDATOR

#ID VALIDATOR
def validateID(P):
    if len(P) <= 8 and (P.isdigit() or keyboard.is_pressed('backspace')):
        return True
    else:
        return False

#PHONE VALIDATOR
def validatePhone(P):
    if (len(P) == 1 and P[0]=='0' or (len(P) == 2 and P[1]=='9') or keyboard.is_pressed('backspace')):
        return True
    elif len(P) >= 3 and len(P) <= 11 and P.isdigit() and P[0] == '0' and P[1] == '9':
        return True
    else: return False

def validateSection(P):
    if ((len(P) <= 3 and P.isdigit()) or keyboard.is_pressed('backspace')):
        return True
    else: return False

#Validator for character input in text entry
idvalid = (root.register(validateID), '%P')
phonevalid = (root.register(validatePhone), '%P')
secvalid = (root.register(validateSection), '%P')

###############################################################################################################################################
#STUDENT VARIABLES AND FUNCTION

#placeholders for entry
setStud1 = tk.StringVar()
setStud2 = tk.StringVar()
setStud3 = tk.StringVar()
setStud4 = tk.StringVar()
setStud5 = tk.StringVar()
setStud6= tk.StringVar()
setStud7 = tk.StringVar()
setStud8 = tk.StringVar()

#Reading all columns in students table
def readStudents():
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM `students`")
    results=cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def refreshTableStudent():
    for data in treeStudent.get_children():
        treeStudent.delete(data)

    for array in readStudents():
        treeStudent.insert(parent='', index='end', iid=array, text='', values=(array), tag='orow')
    
    treeStudent.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))

def addStudent():
    studid=str(txtStudentID.get())
    lname=str(txtSLname.get())
    fname=str(txtSFname.get())
    mname=str(txtSMname.get())
    courseid=str(txtSCourseID.get())
    phone=str(txtSPhone.get())
    email=str(txtSEmail.get())
    address=str(txtSAddress.get())

    if((studid=='' or studid==' ') or (lname=='' or lname==' ') or (fname=='' or fname==' ') or (courseid=='' or courseid==' ') or (phone=='' or phone==' ') or (email=='' or email==' ') or (address=='' or address==' ')):
        messagebox.showinfo('ERROR', 'Please fill up all the blank entry.')
    elif len(studid) != 8:
        messagebox.showinfo('ERROR', 'Please fill up exactly 8 characters for Student ID.')
    elif len(phone) != 11:
        messagebox.showinfo('ERROR', 'Please fill up a valid phone number.')
    else:
        conn=connection()
        cursor=conn.cursor()
        cursor.execute("SELECT COURSEID FROM COURSE WHERE COURSEID = '"+courseid+"'")
        cidresult = cursor.fetchall()
        cursor.execute("SELECT STUDID FROM STUDENTS WHERE STUDID = '"+studid+"'")
        studidresult = cursor.fetchall()
        
        if not cidresult and studidresult :
            messagebox.showinfo('ERROR', '1.) Student ID Already exists \n 2.) Please input a valid course ID')
        elif studidresult:
            messagebox.showinfo('ERROR', 'Student ID Already exists')
        elif not cidresult:
            messagebox.showinfo('ERROR', 'Please input a valid course ID')
        else:
            cursor.execute("INSERT INTO STUDENTS VALUES('"+studid+"', '"+lname+"', '"+fname+"', '"+mname+"', '"+courseid+"', '"+phone+"', '"+email+"', '"+address+"')",)
            conn.commit()
            resetStudent()
        conn.close()
        refreshTableStudent()

def deleteStudent():
    decisionChoices = messagebox.askquestion('Warning!!', 'Do you really want to delete the selected data?')
    if decisionChoices == 'yes':
        selected = treeStudent.selection()
        deleteitem = []
        for record in selected:
            deleteitem.append(treeStudent.item(record, 'values')[0])
        commandquery = 'DELETE FROM STUDENTS WHERE STUDID = %s'
        conn=connection()   
        cursor=conn.cursor()
        cursor.executemany(commandquery, deleteitem)
        conn.commit()
        conn.close()
    else: return
    refreshTableStudent()

def deleteDataStudent():
    decision = messagebox.askquestion("Warning!!", "Delete all data?")
    if decision != "yes":
        return 
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Sorry an error occured")
            return
        refreshTableStudent()

def selectStudent():
    selected = treeStudent.selection()
    if len(selected) == 1:
        for record in selected:
            setStud1.set(treeStudent.item(record, 'values')[0])
            setStud2.set(treeStudent.item(record, 'values')[1])
            setStud3.set(treeStudent.item(record, 'values')[2])
            setStud4.set(treeStudent.item(record, 'values')[3])
            setStud5.set(treeStudent.item(record, 'values')[4])
            setStud6.set(treeStudent.item(record, 'values')[5])
            setStud7.set(treeStudent.item(record, 'values')[6])
            setStud8.set(treeStudent.item(record, 'values')[7])
    else: 
        messagebox.showinfo("Error", "Please select only one row")
    
def searchStudent():
    studid = str(txtStudentID.get())
    lname = str(txtSLname.get())
    fname = str(txtSFname.get())
    mname = str(txtSMname.get())
    courseid=str(txtSCourseID.get())
    phone = str(txtSPhone.get())
    email = str(txtSEmail.get())
    address = str(txtSAddress.get())

    list=[studid, lname, fname, mname, courseid, phone, email,address]
    list2=['studid', 'lname', 'fname', 'mname', 'courseid', 'phone', 'email','address']
    itemsearch = []
    index = []
    for i in range(0, 8):
        if bool(list[i]):
            itemsearch.append(list2[i])
            index.append(i)
    
    if len(index) == 0:
        messagebox.showinfo("Error", "Please input in any field to search.")
        return

    command2 = " "
    for h in range(0, len(index)):
        if(len(index)-1 == h):
            command2 += (list2[index[h]].upper() +"='"+ str(list[index[h]])+"';")
        else:
            command2 += list2[index[h]].upper() +"='"+ str(list[index[h]]) +"' AND " 

    commandquery = 'SELECT * FROM students WHERE '
    conn=connection()   
    cursor=conn.cursor()
    cursor.execute(commandquery + command2)
    results=cursor.fetchall()
    conn.close()

    for data in treeStudent.get_children():
        treeStudent.delete(data)
    
    if len(results) == 0:
        readStudents()
        refreshTableStudent()
        messagebox.showinfo("Error", "Data not found")
    else:
        for arr in results:
            treeStudent.insert(parent='', index='end', iid=arr, text='', values=(arr), tag='orow')

def updateStudent():
    selectedStudid = ""
    try:
        selected_item = treeStudent.selection()[0]
        selectedStudid = str(treeStudent.item(selected_item)['values'][0])
    except:
        messagebox.showinfo("Error", "Please select a data row")
        return

    studid=str(txtStudentID.get())
    lname=str(txtSLname.get())
    fname=str(txtSFname.get())
    mname=str(txtSMname.get())
    courseid=str(txtSCourseID.get())
    phone=str(txtSPhone.get())
    email=str(txtSEmail.get())
    address=str(txtSAddress.get())

    if((studid=='' or studid==' ') or (lname=='' or lname==' ') or (fname=='' or fname==' ') or (courseid=='' or courseid==' ') or (phone=='' or phone==' ') or (email=='' or email==' ') or (address=='' or address==' ')):
        messagebox.showinfo('ERROR', 'Please fill up all the blank entry!')
    elif len(studid) != 8:
        messagebox.showinfo('ERROR', 'Please fill up exactly 8 characters for Student ID.')
    elif len(phone) != 11:
        messagebox.showinfo('ERROR', 'Please fill up a valid phone number.')
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE STUDENTS SET STUDID='"+
            studid+"', LNAME='"+
            lname+"', FNAME='"+
            fname+"', MNAME='"+
            mname+"', COURSEID='"+
            courseid+"', PHONE='"+
            phone+"', EMAIL='"+
            email+"', ADDRESS='"+
            address+"'WHERE STUDID='"+
            selectedStudid+"' ")
            conn.commit()
            resetStudent()
        except:
            cursor.execute("SELECT STUDID FROM STUDENTS WHERE STUDID = '"+studid+"'")
            studidresult = cursor.fetchall()
            cursor.execute("SELECT COURSEID FROM COURSE WHERE COURSEID = '"+courseid+"'")
            courseidresult = cursor.fetchall()
            if studidresult and not courseidresult:
                messagebox.showinfo('ERROR', 'Please input a unique Student ID and a valid Course ID.')
            elif studidresult:
                messagebox.showinfo('ERROR', 'Student ID already exists.')
            else:
                messagebox.showinfo("Error", "Please input a valid Course ID")
        conn.close()
    refreshTableStudent()

def resetStudent():
    setStud1.set('')
    setStud2.set('')
    setStud3.set('')
    setStud4.set('')
    setStud5.set('')
    setStud6.set('')
    setStud7.set('')
    setStud8.set('')

    txtStudentID.configure(validate="key", validatecommand=idvalid)
    txtSCourseID.configure(validate="key", validatecommand=idvalid)
    txtSPhone.configure(validate="key", validatecommand=phonevalid)

def resetTableStudent():
    readStudents()
    refreshTableStudent()

fStudent = ctk.CTkFrame(nbTab, width=1280, height=720, bg='#ECECEC')
fStudent.pack()
treeStudent = ttk.Treeview(fStudent, height=13)
treeStudent.place(x=75,y=363)
nbTab.add(fStudent, text='Student')
#Setting up the label
lblTitle = Label(fStudent,text='School Management System', background='#2E2E2E', foreground='#11B384', font=('Arial bold', 24))
lblTitle.place(x=440, y=10)

lblSLname = ctk.CTkLabel(fStudent, text='Last Name', text_font=('Arial bold', 10), bg='#ECECEC')
lblSFname = ctk.CTkLabel(fStudent, text='First Name', text_font=('Arial bold', 10), bg='#ECECEC')
lblSMname = ctk.CTkLabel(fStudent, text='Middle Name', text_font=('Arial bold', 10), bg='#ECECEC')
lblStudentID = ctk.CTkLabel(fStudent, text='Student ID', text_font=('Arial bold', 10), bg='#ECECEC')
lblSCourseID = ctk.CTkLabel(fStudent, text='Course ID', text_font=('Arial bold', 10), bg='#ECECEC')
lblSPhone = ctk.CTkLabel(fStudent, text='Phone', text_font=('Arial bold', 10), bg='#ECECEC')
lblSEmail = ctk.CTkLabel(fStudent, text='Email', text_font=('Arial bold', 10), bg='#ECECEC')
lblSAddress = ctk.CTkLabel(fStudent, text='Address', text_font=('Arial bold', 10), bg='#ECECEC')

lblSLname.place(x=45, y = 70) 
lblSFname.place(x=210, y = 70)
lblSMname.place(x=380, y = 70)
lblStudentID.place(x=42, y = 140)
lblSCourseID.place(x=207, y = 140)
lblSPhone.place(x=360, y = 140)
lblSEmail.place(x=30, y = 210)
lblSAddress.place(x=283, y = 210)

#Setting for the Entry for input
txtSLname = ctk.CTkEntry(fStudent, width=150,text_font=('Arial', 10), textvariable=setStud2)
txtSFname = ctk.CTkEntry(fStudent, width=150, text_font=('Arial', 10), textvariable=setStud3)
txtSMname = ctk.CTkEntry(fStudent, width=150, bg='white',text_font=('Arial', 10), textvariable=setStud4)
txtStudentID = ctk.CTkEntry(fStudent, width=150,text_font=('Arial', 10), textvariable=setStud1, validate="key", validatecommand=idvalid)
txtSCourseID = ctk.CTkEntry(fStudent, width=150,text_font=('Arial', 10), textvariable=setStud5, validate="key", validatecommand=idvalid)
txtSPhone = ctk.CTkEntry(fStudent, width=150,text_font=('Arial', 10), textvariable=setStud6, validate="key", validatecommand=phonevalid)
txtSEmail = ctk.CTkEntry(fStudent, width=230,text_font=('Arial', 10), textvariable=setStud7)
txtSAddress = ctk.CTkEntry(fStudent, width=230,text_font=('Arial', 10), textvariable=setStud8)

txtSLname.place(x=78, y=100)
txtSFname.place(x=243, y=100)
txtSMname.place(x=408, y=100)
txtStudentID.place(x=78, y=170)
txtSCourseID.place(x=243, y=170)
txtSPhone.place(x=408, y=170)
txtSEmail.place(x=78, y=240)
txtSAddress.place(x=327, y=240)

#Setting for the Button Add, Update and Delete
btnStudAdd = ctk.CTkButton(fStudent,width=100, height=27, text='ADD', text_font=('Arial Bold', 10), command=addStudent)
btnStudUpdate = ctk.CTkButton(fStudent,width=100, height=27, text='UPDATE', text_font=('Arial Bold', 10), command=updateStudent)
btnStudDelete = ctk.CTkButton(fStudent,width=100, height=27, text='DELETE', text_font=('Arial Bold', 10), command=deleteStudent)
btnStudSearch = ctk.CTkButton(fStudent,width=100, height=27, text='SEARCH', text_font=('Arial Bold', 10), command=searchStudent)
btnStudDeleteData = ctk.CTkButton(fStudent,width=100, height=27, text='DELETE ALL', text_font=('Arial Bold', 10), command=deleteDataStudent)
btnStudSelect = ctk.CTkButton(fStudent,width=100, height=27, text='SELECT',  text_font=('Arial Bold', 10), command=selectStudent)
btnSReset = ctk.CTkButton(fStudent,width=100, height=27, text='RESET ENTRY',  text_font=('Arial Bold', 10), command=resetStudent)
btnSResetTable = ctk.CTkButton(fStudent,width=100, height=27, text='RESET TABLE',  text_font=('Arial Bold', 10), command=resetTableStudent)

btnStudAdd.place(x=572, y = 102)
btnStudUpdate.place(x=572, y = 172)
btnStudDelete.place(x=572, y = 242)
btnStudSearch.place(x=687, y = 102)
btnStudDeleteData.place(x=687, y = 172)
btnStudSelect.place(x=687, y = 242)
btnSReset.place(x=78, y=285)
btnSResetTable.place(x=200, y=285)

#STUDENT RECORDS LABEL
lblStudentRecords = Label(fStudent,text='Students Record', background='#2E2E2E', foreground='#11B384', font=('Arial Bold', 20))
lblStudentRecords.place(x=520, y=310)

# Read the Image
image = Image.open("PUP2.jpg")
imgPUP = ImageTk.PhotoImage(image.resize((392, 197)))
 
# create label and add resize image
label1 = ctk.CTkLabel(fStudent,image=imgPUP)   
label1.image = imgPUP
label1.place(x=808, y=72)
 
#Styling the treeview in Student
style=ttk.Style()
style.theme_use('clam')
style.configure("Treeview.Heading", font=('Arial Bold', 10), foreground='#11B384', background='#2E2E2E')

treeStudent['columns']=('StudID', 'LastName', 'FirstName', 'MiddleName', 'CourseID', 'Phone', 'Email', 'Address')

treeStudent.column('#0', width=0, stretch=NO)
treeStudent.column('StudID', anchor=W, width=95)
treeStudent.column('LastName', anchor=W, width=120)
treeStudent.column('FirstName', anchor=W, width=120)
treeStudent.column('MiddleName', anchor=W, width=120)
treeStudent.column('CourseID', anchor=W, width=95)
treeStudent.column('Phone', anchor=W, width=120)
treeStudent.column('Email', anchor=W, width=200)
treeStudent.column('Address', anchor=W, width=250)


treeStudent.heading('StudID', text='Student ID', anchor=W)
treeStudent.heading('LastName', text='Last Name', anchor=W)
treeStudent.heading('FirstName', text='First Name', anchor=W)
treeStudent.heading('MiddleName', text='Middle Name', anchor=W)
treeStudent.heading('CourseID', text='Course ID', anchor=W)
treeStudent.heading('Phone', text='Phone', anchor=W)
treeStudent.heading('Email', text='Email', anchor=W)
treeStudent.heading('Address', text='Address', anchor=W)

refreshTableStudent()
##############################################################################################################################################
#INSTRUCTOR TAB         #INSTRUCTOR TAB             #INSTRUCTOR TAB                 #INSTRUCTOR TAB                 #INSTRUCTOR TAB
#placeholders for entry
setIns1 = tk.StringVar()
setIns2 = tk.StringVar()
setIns3 = tk.StringVar()
setIns4 = tk.StringVar()
setIns5 = tk.StringVar()
setIns6 = tk.StringVar()

def refreshTableInstructor():
    for data in treeInstructor.get_children():
        treeInstructor.delete(data)

    for array in readInstructor():
        treeInstructor.insert(parent='', index='end', iid=array, text='', values=(array), tag='orow')
    
    treeInstructor.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))

#Reading all columns in instructor table
def readInstructor():
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM `INSTRUCTOR`")
    results=cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def addInstructor():
    instructorid=str(txtInstructorID.get())
    lname=str(txtILname.get())
    fname=str(txtIFname.get())
    mname=str(txtIMname.get())
    phone=str(txtIPhone.get())
    email=str(txtIEmail.get())

    if((instructorid=='' or instructorid==' ') or (lname=='' or lname==' ') or (fname=='' or fname==' ') or (phone=='' or phone==' ') or (email=='' or email==' ')):
        messagebox.showinfo('ERROR', 'Please fill up all the blank entry!')
    elif len(instructorid) != 8:
        messagebox.showinfo('ERROR', 'Please fill up exactly 8 characters for Instructor ID.')
    elif len(phone) != 11:
        messagebox.showinfo('ERROR', 'Please fill up a valid phone number.')
    else:
        conn=connection()
        cursor=conn.cursor()
        cursor.execute("SELECT INSTRUCTORID FROM INSTRUCTOR WHERE INSTRUCTORID = '"+instructorid+"'")
        instructoridresult = cursor.fetchall()
     
        if instructoridresult:
            messagebox.showinfo('ERROR', 'Instructor ID Already exists')
        else:
            cursor.execute("INSERT INTO INSTRUCTOR VALUES('"+instructorid+"', '"+lname+"', '"+fname+"', '"+mname+"', '"+phone+"', '"+email+"')",)
            conn.commit()
            resetInstructor()
        conn.close()
        refreshTableInstructor()

def deleteInstructor():
    decisionChoices = messagebox.askquestion('Warning!!', 'Do you really want to delete the selected data?')
    if decisionChoices == 'yes':
        try:
            selected = treeInstructor.selection()
            deleteitem = []
            for record in selected:
                deleteitem.append(treeInstructor.item(record, 'values')[0])
            commandquery = 'DELETE FROM INSTRUCTOR WHERE INSTRUCTORID = %s'
            conn=connection()   
            cursor=conn.cursor()
            cursor.executemany(commandquery, deleteitem)
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo('ERROR', "Can't be deleted. It might affect other table")
            return
    refreshTableInstructor()

def deleteDataInstructor():
    decision = messagebox.askquestion("Warning!!", "Delete all data?")
    if decision != "yes":
        return 
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM INSTRUCTOR")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Sorry an error occured")
            return
        refreshTableInstructor()

def selectInstructor():
    selected = treeInstructor.selection()
    if len(selected) == 1:
        for record in selected:
            setIns1.set(treeInstructor.item(record, 'values')[0])
            setIns2.set(treeInstructor.item(record, 'values')[1])
            setIns3.set(treeInstructor.item(record, 'values')[2])
            setIns4.set(treeInstructor.item(record, 'values')[3])
            setIns5.set(treeInstructor.item(record, 'values')[4])
            setIns6.set(treeInstructor.item(record, 'values')[5])
    else:
        messagebox.showinfo("Error", "Please select only one row") 

def searchInstructor():
    instructorid=str(txtInstructorID.get())
    lname=str(txtILname.get())
    fname=str(txtIFname.get())
    mname=str(txtIMname.get())
    phone=str(txtIPhone.get())
    email=str(txtIEmail.get())

    list=[instructorid, lname, fname, mname, phone, email]
    list2=['instructorid', 'lname', 'fname', 'mname', 'phone', 'email']
    itemsearch = []
    index = []
    command2 = " "

    for i in range(0, 6):
        if bool(list[i]):
            itemsearch.append(list2[i])
            index.append(i)
    
    if len(index) == 0:
        messagebox.showinfo("Error", "Please input in any field to search.")
        return

    for h in range(0, len(index)):
        if(len(index)-1 == h):
            command2 += (list2[index[h]].upper() +"='"+ str(list[index[h]])+"';")
        else:
            command2 += list2[index[h]].upper() +"='"+ str(list[index[h]]) +"' AND " 

    commandquery = 'SELECT * FROM INSTRUCTOR WHERE '
    conn=connection()   
    cursor=conn.cursor()
    cursor.execute(commandquery + command2)
    results=cursor.fetchall()
    conn.close()

    for data in treeInstructor.get_children():
        treeInstructor.delete(data)
    
    if len(results) == 0:
        readInstructor()
        refreshTableInstructor()
        messagebox.showinfo("Error", "Data not found")
    else:
        for arr in results:
            treeInstructor.insert(parent='', index='end', iid=arr, text='', values=(arr), tag='orow')

def updateInstructor():
    selectedInstructorid = ""
    try:
        selected_item = treeInstructor.selection()[0]
        selectedInstructorid = str(treeInstructor.item(selected_item)['values'][0])
    except:
        messagebox.showinfo("Error", "Please select a data row")
        return

    instructorid=str(txtInstructorID.get())
    lname=str(txtILname.get())
    fname=str(txtIFname.get())
    mname=str(txtIMname.get())
    phone=str(txtIPhone.get())
    email=str(txtIEmail.get())

    if((instructorid=='' or instructorid==' ') or (lname=='' or lname==' ') or (fname=='' or fname==' ') or (phone=='' or phone==' ') or (email=='' or email==' ')):
        messagebox.showinfo('ERROR', 'Please fill up all the blank entry!')
    elif len(instructorid) != 8:
        messagebox.showinfo('ERROR', 'Please fill up exactly 8 characters for Instructor ID.')
    elif len(phone) != 11:
        messagebox.showinfo('ERROR', 'Please fill up a valid phone number.')
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE INSTRUCTOR SET INSTRUCTORID='"+
            instructorid+"', LNAME='"+
            lname+"', FNAME='"+
            fname+"', MNAME='"+
            mname+"', PHONE='"+
            phone+"', EMAIL='"+
            email+"'WHERE INSTRUCTORID='"+
            selectedInstructorid+"' ")
            conn.commit()
            resetInstructor()
        except:
            cursor.execute("SELECT INSTRUCTORID FROM INSTRUCTOR WHERE INSTRUCTORID = '"+instructorid+"'")
            instructoridresult = cursor.fetchall()
            if instructoridresult:
                messagebox.showinfo('ERROR', 'Instructor ID Already exists')
            else:
                messagebox.showinfo("Error", "Can't update the ID. This might affect the other table.")
        conn.close()
    refreshTableInstructor()

def resetInstructor():
    setIns1.set('')
    setIns2.set('')
    setIns3.set('')
    setIns4.set('')
    setIns5.set('')
    setIns6.set('')

    txtInstructorID.configure(validate="key", validatecommand=idvalid)
    txtIPhone.configure(validate="key", validatecommand=phonevalid)

def resetTableInstructor():
    readInstructor()
    refreshTableInstructor()

fInstructor = ctk.CTkFrame(nbTab, width=1280, height=720, bg="#ECECEC")
fInstructor.pack()
treeInstructor = ttk.Treeview(fInstructor, height=13)
treeInstructor.place(x=75,y=363)
nbTab.add(fInstructor, text='Instructor')

lblTitle = Label(fInstructor,text='School Management System', background='#2E2E2E', foreground='#11B384', font=('Arial bold', 24))
lblTitle.place(x=440, y=10)

lblILname = ctk.CTkLabel(fInstructor, text='Last Name', text_font=('Arial bold', 10), bg='#ECECEC')
lblIFName = ctk.CTkLabel(fInstructor, text='First Name', text_font=('Arial bold', 10), bg='#ECECEC')
lblIMName = ctk.CTkLabel(fInstructor, text='Middle Name', text_font=('Arial bold', 10), bg='#ECECEC')
lblInstructorID = ctk.CTkLabel(fInstructor, text='Instructor ID', text_font=('Arial bold', 10), bg='#ECECEC')
lblIPhone = ctk.CTkLabel(fInstructor, text='Phone', text_font=('Arial bold', 10), bg='#ECECEC')
lblIEmail = ctk.CTkLabel(fInstructor, text='Email', text_font=('Arial bold', 10), bg='#ECECEC')

lblILname.place(x=45, y = 70) 
lblIFName.place(x=210, y = 70)
lblIMName.place(x=380, y = 70)
lblInstructorID.place(x=50, y = 140)
lblIPhone.place(x=280, y = 140)
lblIEmail.place(x=29, y = 210)
#lblSEmail.place(x=30, y = 210)
#lblSAddress.place(x=283, y = 210)

#Setting for the Entry for input
txtILname = ctk.CTkEntry(fInstructor, width=150,text_font=('Arial', 10), textvariable=setIns2)
txtIFname = ctk.CTkEntry(fInstructor, width=150, text_font=('Arial', 10), textvariable=setIns3)
txtIMname = ctk.CTkEntry(fInstructor, width=150, bg='white',text_font=('Arial', 10), textvariable=setIns4)
txtInstructorID = ctk.CTkEntry(fInstructor, width=230,text_font=('Arial', 10), textvariable=setIns1, validate="key", validatecommand=idvalid)
txtIPhone = ctk.CTkEntry(fInstructor, width=230,text_font=('Arial', 10), textvariable=setIns5,validate="key", validatecommand=phonevalid)
txtIEmail = ctk.CTkEntry(fInstructor, width=478,text_font=('Arial', 10), textvariable=setIns6)

txtILname.place(x=78, y=100)
txtIFname.place(x=243, y=100)
txtIMname.place(x=408, y=100)
txtInstructorID.place(x=78, y=170)
txtIPhone.place(x=327, y=170)
txtIEmail.place(x=78, y=240)

#Setting for the Button Add, Update and Delete
btnInsAdd = ctk.CTkButton(fInstructor,width=100, height=27, text='ADD', text_font=('Arial Bold', 10), command=addInstructor)
btnInsUpdate = ctk.CTkButton(fInstructor,width=100, height=27, text='UPDATE', text_font=('Arial Bold', 10), command=updateInstructor)
btnInsDelete = ctk.CTkButton(fInstructor,width=100, height=27, text='DELETE', text_font=('Arial Bold', 10), command=deleteInstructor)
btnInsSearch = ctk.CTkButton(fInstructor,width=100, height=27, text='SEARCH', text_font=('Arial Bold', 10), command=searchInstructor)
btnInsDeleteData = ctk.CTkButton(fInstructor,width=100, height=27, text='DELETE ALL', text_font=('Arial Bold', 10), command=deleteDataInstructor)
btnInsSelect = ctk.CTkButton(fInstructor,width=100, height=27, text='SELECT',  text_font=('Arial Bold', 10), command=selectInstructor)
btnInsReset = ctk.CTkButton(fInstructor,width=100, height=27, text='RESET ENTRY',  text_font=('Arial Bold', 10), command=resetInstructor)
btnSResetTable = ctk.CTkButton(fInstructor,width=100, height=27, text='RESET TABLE',  text_font=('Arial Bold', 10), command=resetTableInstructor)

btnInsAdd.place(x=572, y = 102)
btnInsUpdate.place(x=572, y = 172)
btnInsDelete.place(x=572, y = 242)
btnInsSearch.place(x=687, y = 102)
btnInsDeleteData.place(x=687, y = 172)
btnInsSelect.place(x=687, y = 242)
btnInsReset.place(x=78, y=285)
btnSResetTable.place(x=200, y=285)

#INSTRUCTOR RECORDS LABEL
lblInsructorRecords = Label(fInstructor,text='Instructor Records', background='#2E2E2E', foreground='#11B384', font=('Arial Bold', 20))
lblInsructorRecords.place(x=520, y=310)

# Read the Image
image = Image.open("PUP2.jpg")
imgPUP = ImageTk.PhotoImage(image.resize((392, 197)))
 
# create label and add resize image
label1 = ctk.CTkLabel(fInstructor,image=imgPUP)   
label1.image = imgPUP
label1.place(x=808, y=72)
treeInstructor['columns']=('InstructorID', 'LastName', 'FirstName', 'MiddleName', 'Phone', 'Email')

treeInstructor.column('#0', width=0, stretch=NO)
treeInstructor.column('InstructorID', anchor=W, width=164)
treeInstructor.column('LastName', anchor=W, width=164)
treeInstructor.column('FirstName', anchor=W, width=164)
treeInstructor.column('MiddleName', anchor=W, width=164)
treeInstructor.column('Phone', anchor=W, width=164)
treeInstructor.column('Email', anchor=W, width=300)


treeInstructor.heading('InstructorID', text='Instructor ID', anchor=W)
treeInstructor.heading('LastName', text='Last Name', anchor=W)
treeInstructor.heading('FirstName', text='First Name', anchor=W)
treeInstructor.heading('MiddleName', text='Middle Name', anchor=W)
treeInstructor.heading('Phone', text='Phone', anchor=W)
treeInstructor.heading('Email', text='Email', anchor=W)

refreshTableInstructor()
##############################################################################################################################################
#SECTION TAB
#placeholders for entry
setSec1 = tk.StringVar()
setSec2 = tk.StringVar()
setSec3 = tk.StringVar()
setSec4 = tk.StringVar()

def readSection():
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM `SECTION`")
    results=cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def refreshTableSection():
    for data in treeSection.get_children():
        treeSection.delete(data)

    for array in readSection():
        treeSection.insert(parent='', index='end', iid=array, text='', values=(array), tag='orow')
    
    treeSection.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))

def addSection():
    sectionno=str(txtSectionNo.get())
    courseid=str(txtSecCourseID.get())
    daytime=str(txtSecDayTime.get())
    location=str(txtSecLocation.get())

    if((sectionno=='' or sectionno==' ') or (courseid=='' or courseid==' ') or (daytime=='' or daytime==' ') or (location=='' or location==' ')):
        messagebox.showinfo('ERROR', 'Please fill up all the blank entry!')
    elif sectionno == '0' or sectionno == '00' or sectionno == '000':
        messagebox.showinfo('ERROR', 'Section Number must contain a number')
    else:
        conn=connection()
        cursor=conn.cursor()
        cursor.execute("SELECT COURSEID FROM COURSE WHERE COURSEID = '"+courseid+"'")
        cidresult = cursor.fetchall()
        cursor.execute("SELECT SECTIONNO FROM SECTION WHERE SECTIONNO = '"+sectionno+"'")
        sectionnoresult = cursor.fetchall()
        
        if not cidresult and sectionnoresult :
            messagebox.showinfo('ERROR', '1.) Section number already exists \n 2.) Please input a valid course ID')
        elif sectionnoresult:
            messagebox.showinfo('ERROR', 'Section number already exists')
        elif not cidresult:
            messagebox.showinfo('ERROR', 'Please input a valid course ID')
        else:
            cursor.execute("INSERT INTO SECTION VALUES('"+sectionno+"', '"+courseid+"', '"+daytime+"', '"+location+"')",)
            conn.commit()
            resetSection()
        conn.close()
        refreshTableSection()

def deleteSection():
    decisionChoices = messagebox.askquestion('Warning!!', 'Do you really want to delete the selected data?')
    if decisionChoices == 'yes':
        try: 
            selected = treeSection.selection()
            deleteitem = []
            for record in selected:
                deleteitem.append(treeSection.item(record, 'values')[0])
            commandquery = 'DELETE FROM SECTION WHERE SECTIONNO = %s'
            conn=connection()   
            cursor=conn.cursor()
            cursor.executemany(commandquery, deleteitem)
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo('ERROR', "Can't be deleted. It might affect other table")
            return
    refreshTableSection()

def deleteDataSection():
    decision = messagebox.askquestion("Warning!!", "Delete all data?")
    if decision != "yes":
        return 
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM SECTION")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Sorry an error occured")
            return
        refreshTableSection()

def selectSection():
    selected = treeSection.selection()
    if len(selected) == 1:
        for record in selected:
            setSec1.set(treeSection.item(record, 'values')[0])
            setSec2.set(treeSection.item(record, 'values')[1])
            setSec3.set(treeSection.item(record, 'values')[2])
            setSec4.set(treeSection.item(record, 'values')[3])
    else: 
        messagebox.showinfo("Error", "Please select only one row")

def searchSection():
    sectionno=str(txtSectionNo.get())
    courseid=str(txtSecCourseID.get())
    daytime=str(txtSecDayTime.get())
    location=str(txtSecLocation.get())

    list=[sectionno, courseid, daytime, location]
    list2=['sectionno', 'courseid', 'daytime', 'location']
    itemsearch = []
    index = []
    command2 = " "

    for i in range(0, 4):
        if bool(list[i]):
            itemsearch.append(list2[i])
            index.append(i)

    if len(index) == 0:
        messagebox.showinfo("Error", "Please input in any field to search.")
        return

    for h in range(0, len(index)):
        if(len(index)-1 == h):
            if(list2[index[h]].upper() == 'SECTIONNO'):
                command2 += list2[index[h]].upper() +"="+ (list[index[h]]) +";"
            else:
                command2 += (list2[index[h]].upper() +"='"+ str(list[index[h]])+"';")
        else:
            if(list2[index[h]].upper() == 'SECTIONNO'):
                command2 += list2[index[h]].upper() +"="+ (list[index[h]]) +" AND "
            else:
                command2 += list2[index[h]].upper() +"='"+ str(list[index[h]]) +"' AND " 

    commandquery = 'SELECT * FROM SECTION WHERE '
    conn=connection()   
    cursor=conn.cursor()
    cursor.execute(commandquery + command2)
    results=cursor.fetchall()
    conn.close()

    for data in treeSection.get_children():
        treeSection.delete(data)
    
    if len(results) == 0:
        readSection()
        refreshTableSection()
        messagebox.showinfo("Error", "Data not found")
    else:
        for arr in results:
            treeSection.insert(parent='', index='end', iid=arr, text='', values=(arr), tag='orow')

def updateSection():
    selectedSectionNo = ""
    try:
        selected_item = treeSection.selection()[0]
        selectedSectionNo = str(treeSection.item(selected_item)['values'][0])
    except:
        messagebox.showinfo("Error", "Please select a data row")
        return

    sectionno=str(txtSectionNo.get())
    courseid=str(txtSecCourseID.get())
    daytime=str(txtSecDayTime.get())
    location=str(txtSecLocation.get())

    if((sectionno=='' or sectionno==' ') or (courseid=='' or courseid==' ') or (daytime=='' or daytime==' ') or (location=='' or location==' ')):
        messagebox.showinfo('ERROR', 'Please fill up all the blank entry!')
    elif sectionno == '0' or sectionno == '00' or sectionno == '000':
        messagebox.showinfo('ERROR', 'Section Number must contain a number')
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE SECTION SET SECTIONNO='"+
            sectionno+"', COURSEID='"+
            courseid+"', DAYTIME='"+
            daytime+"', LOCATION='"+
            location+"'WHERE SECTIONNO='"+
            selectedSectionNo+"' ")
            conn.commit()
            resetSection()
        except:
            cursor.execute("SELECT SECTIONNO FROM SECTION WHERE SECTIONNO = '"+sectionno+"'")
            sectionnoresult = cursor.fetchall()
            cursor.execute("SELECT COURSEID FROM COURSE WHERE COURSEID = '"+courseid+"'")
            cidresult = cursor.fetchall()
            if not cidresult and sectionnoresult :
                messagebox.showinfo('ERROR', '1.) Section number already exists \n 2.) Please input a valid course ID')
            elif sectionnoresult:
                messagebox.showinfo('ERROR', 'Section number already exists')
            else:
                messagebox.showinfo('ERROR', 'Please input a valid course ID')
        conn.close()
    refreshTableSection()

def resetSection():
    setSec1.set('')
    setSec2.set('')
    setSec3.set('')
    setSec4.set('')

    txtSecCourseID.configure(validate="key", validatecommand=idvalid)
    txtSectionNo.configure(validate="key", validatecommand=secvalid)

def resetTableSection():
    readSection()
    refreshTableSection()


fSection = ctk.CTkFrame(nbTab, width=1280, height=720, bg="#ECECEC")
fSection.pack()
treeSection = ttk.Treeview(fSection, height=13)
treeSection.place(x=75,y=363)
nbTab.add(fSection, text='Section')

lblTitle = Label(fSection,text='School Management System', background='#2E2E2E', foreground='#11B384', font=('Arial bold', 24))
lblTitle.place(x=440, y=10)

lblSectionNo = ctk.CTkLabel(fSection, text='Section No.', text_font=('Arial bold', 10), bg='#ECECEC')
lblSecCourseID = ctk.CTkLabel(fSection, text='Course ID', text_font=('Arial bold', 10), bg='#ECECEC')
lblSecDayTime = ctk.CTkLabel(fSection, text='Day Time', text_font=('Arial bold', 10), bg='#ECECEC')
lblSecLocation = ctk.CTkLabel(fSection, text='Location', text_font=('Arial bold', 10), bg='#ECECEC')

lblSectionNo.place(x=44, y = 70) 
lblSecCourseID.place(x=205, y = 70)
lblSecDayTime.place(x=370, y = 70)
lblSecLocation.place(x=37, y = 140)

txtSectionNo = ctk.CTkEntry(fSection, width=150,text_font=('Arial', 10),textvariable=setSec1, validate="key", validatecommand=secvalid)
txtSecCourseID = ctk.CTkEntry(fSection, width=150, text_font=('Arial', 10),textvariable=setSec2, validate="key", validatecommand=idvalid)
txtSecDayTime = ctk.CTkEntry(fSection, width=150, bg='white',text_font=('Arial', 10),textvariable=setSec3)
txtSecLocation = ctk.CTkEntry(fSection, width=478,text_font=('Arial', 10),textvariable=setSec4)

txtSectionNo.place(x=78, y=100)
txtSecCourseID.place(x=243, y=100)
txtSecDayTime.place(x=408, y=100)
txtSecLocation.place(x=78, y=170)

#Setting for the Button Add, Update and Delete
btnSecAdd = ctk.CTkButton(fSection,width=100, height=27, text='ADD', text_font=('Arial Bold', 10), command=addSection)
btnSecUpdate = ctk.CTkButton(fSection,width=100, height=27, text='UPDATE', text_font=('Arial Bold', 10), command=updateSection)
btnSecDelete = ctk.CTkButton(fSection,width=100, height=27, text='DELETE', text_font=('Arial Bold', 10), command=deleteSection)
btnSecSearch = ctk.CTkButton(fSection,width=100, height=27, text='SEARCH', text_font=('Arial Bold', 10), command=searchSection)
btnSecDeleteAll = ctk.CTkButton(fSection,width=100, height=27, text='DELETE ALL', text_font=('Arial Bold', 10), command=deleteDataSection)
btnSecSelect = ctk.CTkButton(fSection,width=100, height=27, text='SELECT',  text_font=('Arial Bold', 10), command=selectSection)
btnSecReset = ctk.CTkButton(fSection,width=100, height=27, text='RESET ENTRY',  text_font=('Arial Bold', 10), command=resetSection)
btnSecResetTable = ctk.CTkButton(fSection,width=100, height=27, text='RESET TABLE',  text_font=('Arial Bold', 10), command=resetTableSection)

btnSecAdd.place(x=572, y = 102)
btnSecUpdate.place(x=572, y = 172)
btnSecDelete.place(x=572, y = 242)
btnSecSearch.place(x=687, y = 102)
btnSecDeleteAll.place(x=687, y = 172)
btnSecSelect.place(x=687, y = 242)
btnSecReset.place(x=78, y=218)
btnSecResetTable.place(x=200, y=218)

lblSectionRecords = Label(fSection,text='Section Records', background='#2E2E2E', foreground='#11B384', font=('Arial Bold', 20))
lblSectionRecords.place(x=520, y=310)

# Read the Image
image = Image.open("PUP2.jpg")
imgPUP = ImageTk.PhotoImage(image.resize((385, 197)))
 
# create label and add resize image
label1 = ctk.CTkLabel(fSection,image=imgPUP)   
label1.image = imgPUP
label1.place(x=808, y=72)
 
treeSection['columns']=('SectionNo', 'CourseID', 'DayTime', 'Location')

treeSection.column('#0', width=0, stretch=NO)
treeSection.column('SectionNo', anchor=W, width=200)
treeSection.column('CourseID', anchor=W, width=200)
treeSection.column('DayTime', anchor=W, width=200)
treeSection.column('Location', anchor=W, width=520)

treeSection.heading('SectionNo', text='Section Number', anchor=W)
treeSection.heading('CourseID', text='Course ID', anchor=W)
treeSection.heading('DayTime', text='Day Time', anchor=W)
treeSection.heading('Location', text='Location', anchor=W)
refreshTableSection()
##############################################################################################################################################
#placeholders for entry
setCourse1 = tk.StringVar()
setCourse2 = tk.StringVar()

def readCourse():
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM `COURSE`")
    results=cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def refreshTableCourse():
    for data in treeCourse.get_children():
        treeCourse.delete(data)

    for array in readCourse():
        treeCourse.insert(parent='', index='end', iid=array, text='', values=(array), tag='orow')
    
    treeCourse.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))

def addCourse():
    courseid=str(txtCourseID.get())
    coursename=str(txtCourseName.get())

    if((courseid=='' or courseid==' ') or (coursename=='' or coursename==' ')):
        messagebox.showinfo('ERROR', 'Please fill up all the blank entry!')
    elif len(courseid) != 8:
        messagebox.showinfo('ERROR', 'Course ID must contain 8 numbers in the field.')
    else:
        conn=connection()
        cursor=conn.cursor()
        cursor.execute("SELECT COURSEID FROM COURSE WHERE COURSEID = '"+courseid+"'")
        cidresult = cursor.fetchall()
        if cidresult:
            messagebox.showinfo('ERROR', 'Course ID Already exists')
        else:
            cursor.execute("INSERT INTO COURSE VALUES('"+courseid+"', '"+coursename+"')",)
            conn.commit()
            resetCourse()
        conn.close()
        refreshTableCourse()

def deleteCourse():
    decisionChoices = messagebox.askquestion('Warning!!', 'Do you really want to delete the selected data?')
    if decisionChoices == 'yes':
        try: 
            selected = treeCourse.selection()
            deleteitem = []
            for record in selected:
                deleteitem.append(treeCourse.item(record, 'values')[0])
            commandquery = 'DELETE FROM COURSE WHERE COURSEID = %s'
            conn=connection()   
            cursor=conn.cursor()
            cursor.executemany(commandquery, deleteitem)
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo('ERROR', "Can't be deleted. It might affect other table")
            return
    refreshTableCourse()

def deleteDataCourse():
    decision = messagebox.askquestion("Warning!!", "Delete all data?")
    if decision != "yes":
        return 
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM COURSE")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Sorry an error occured")
            return
        refreshTableCourse()

def selectCourse():
    selected = treeCourse.selection()
    if len(selected) == 1:
        for record in selected:
            setCourse1.set(treeCourse.item(record, 'values')[0])
            setCourse2.set(treeCourse.item(record, 'values')[1])
    else: 
        messagebox.showinfo("Error", "Please select only one row")

def searchCourse():
    courseid=str(txtCourseID.get())
    coursename=str(txtCourseName.get())

    list=[courseid, coursename]
    list2=['courseid', 'coursename']
    itemsearch = []
    index = []
    command2 = " "
    for i in range(0, 2):
        if bool(list[i]):
            itemsearch.append(list2[i])
            index.append(i)
    
    if len(index) == 0:
        messagebox.showinfo("Error", "Please input in any field to search.")
        return

    for h in range(0, len(index)):
        if(len(index)-1 == h):
            command2 += (list2[index[h]].upper() +"='"+ str(list[index[h]])+"';")
        else:
            command2 += list2[index[h]].upper() +"='"+ str(list[index[h]]) +"' AND " 

    commandquery = 'SELECT * FROM COURSE WHERE '
    conn=connection()   
    cursor=conn.cursor()
    cursor.execute(commandquery + command2)
    results=cursor.fetchall()
    conn.close()

    for data in treeCourse.get_children():
        treeCourse.delete(data)
    
    if len(results) == 0:
        readCourse()
        refreshTableCourse()
        messagebox.showinfo("Error", "Data not found")
    else:
        for arr in results:
            treeCourse.insert(parent='', index='end', iid=arr, text='', values=(arr), tag='orow')

def updateCourse():
    selectedCourseID = ""
    try:
        selected_item = treeCourse.selection()[0]
        selectedCourseID = str(treeCourse.item(selected_item)['values'][0])
    except:
        messagebox.showinfo("Error", "Please select a data row")
        return

    courseid=str(txtCourseID.get())
    coursename=str(txtCourseName.get())

    if((courseid=='' or courseid==' ') or (coursename=='' or coursename==' ')):
        messagebox.showinfo('ERROR', 'Please fill up all the blank entry!')
    elif len(courseid) != 8:
        messagebox.showinfo('ERROR', 'Course ID must contain 8 numbers in the field.')
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE COURSE SET COURSEID='"+
            courseid+"', COURSENAME='"+
            coursename+"'WHERE COURSEID='"+
            selectedCourseID+"' ")
            conn.commit()
            resetCourse()
        except:
            cursor.execute("SELECT COURSEID FROM COURSE WHERE COURSEID = '"+courseid+"'")
            courseidresult = cursor.fetchall()
            if courseidresult:
                messagebox.showinfo('ERROR', 'Course ID already exists')
            else:
                messagebox.showinfo("Error", "Can't update the Course ID. This might affect the other table.")
        conn.close()
    refreshTableCourse()

def resetCourse():
    setCourse1.set('')
    setCourse2.set('')

    txtCourseID.configure(validate="key", validatecommand=idvalid)

def resetTableCourse():
    readCourse()
    refreshTableCourse()

fCourse = ctk.CTkFrame(nbTab, width=1280, height=720, bg="#ECECEC")
fCourse.pack()
treeCourse = ttk.Treeview(fCourse, height=13)
treeCourse.place(x=75,y=363)
nbTab.add(fCourse, text='Course')

lblTitle = Label(fCourse,text='School Management System', background='#2E2E2E', foreground='#11B384', font=('Arial bold', 24))
lblTitle.place(x=440, y=10)

lblCourseID = ctk.CTkLabel(fCourse, text='Course ID', text_font=('Arial bold', 10), bg='#ECECEC')
lblCourseName = ctk.CTkLabel(fCourse, text='Course Name', text_font=('Arial bold', 10), bg='#ECECEC')

lblCourseID.place(x=42, y = 70) 
lblCourseName.place(x=52, y = 140)

txtCourseID = ctk.CTkEntry(fCourse, width=460,text_font=('Arial', 10),textvariable=setCourse1, validate="key", validatecommand=idvalid)
txtCourseName = ctk.CTkEntry(fCourse, width=460, text_font=('Arial', 10),textvariable=setCourse2)

txtCourseID.place(x=78, y=100)
txtCourseName.place(x=78, y=170)

#Setting for the Button Add, Update and Delete
btnCourseAdd = ctk.CTkButton(fCourse,width=100, height=27, text='ADD', text_font=('Arial Bold', 10), command=addCourse)
btbCourseUpdate = ctk.CTkButton(fCourse,width=100, height=27, text='UPDATE', text_font=('Arial Bold', 10), command=updateCourse)
btbCourseDelete = ctk.CTkButton(fCourse,width=100, height=27, text='DELETE', text_font=('Arial Bold', 10), command=deleteCourse)
btbCourseSearch = ctk.CTkButton(fCourse,width=100, height=27, text='SEARCH', text_font=('Arial Bold', 10), command=searchCourse)
btbCourseDeleteAll = ctk.CTkButton(fCourse,width=100, height=27, text='DELETE ALL', text_font=('Arial Bold', 10), command=deleteDataCourse)
btbCourseSelect = ctk.CTkButton(fCourse,width=100, height=27, text='SELECT',  text_font=('Arial Bold', 10), command=selectCourse)
btbCourseReset = ctk.CTkButton(fCourse,width=100, height=27, text='RESET ENTRY',  text_font=('Arial Bold', 10), command=resetCourse)
btnCourseResetTable = ctk.CTkButton(fCourse,width=100, height=27, text='RESET TABLE',  text_font=('Arial Bold', 10), command=resetTableCourse)

btnCourseAdd.place(x=572, y = 102)
btbCourseUpdate.place(x=572, y = 172)
btbCourseDelete.place(x=572, y = 242)
btbCourseSearch.place(x=687, y = 102)
btbCourseDeleteAll.place(x=687, y = 172)
btbCourseSelect.place(x=687, y = 242)
btbCourseReset.place(x=78, y=218)
btnCourseResetTable.place(x=200, y=218)

lblCourseRecords = Label(fCourse,text='Course Records', background='#2E2E2E', foreground='#11B384', font=('Arial Bold', 20))
lblCourseRecords.place(x=520, y=310)

# Read the Image
image = Image.open("PUP2.jpg")
imgPUP = ImageTk.PhotoImage(image.resize((392, 197)))
 
# create label and add resize image
label1 = ctk.CTkLabel(fCourse,image=imgPUP)   
label1.image = imgPUP
label1.place(x=808, y=72)
 
treeCourse['columns']=('CourseID', 'CourseName')

treeCourse.column('#0', width=0, stretch=NO)
treeCourse.column('CourseID', anchor=W, width=208)
treeCourse.column('CourseName', anchor=W, width=912)

treeCourse.heading('CourseID', text='Course ID', anchor=W)
treeCourse.heading('CourseName', text='Course Name', anchor=W)

refreshTableCourse()

##############################################################################################################################################

setAssign1 = tk.StringVar()
setAssign2 = tk.StringVar()
setAssign3 = tk.StringVar()

def refreshTableAssign():
    for data in treeAssign.get_children():
        treeAssign.delete(data)

    for array in readAssign():
        treeAssign.insert(parent='', index='end', iid=array, text='', values=(array), tag='orow')
    
    treeAssign.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))

def readAssign():
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM `ASSIGN`")
    results=cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def addAssign():
    instructorid=str(txtAInstructorID.get())
    sectionno=str(txtASectionNo.get())
    subject=str(txtASubject.get())

    if((instructorid=='' or instructorid==' ') or (sectionno=='' or sectionno==' ') or (subject=='' or subject==' ')):
        messagebox.showinfo('ERROR', 'Please fill up all the blank entry!')
    elif len(instructorid) != 8 and (sectionno == '0' or sectionno == '00' or sectionno == '000'):
        messagebox.showinfo('ERROR', 'Instructor ID must contain 8 characters in the field and the Section Number must not be 0')
    elif sectionno == '0' or sectionno == '00' or sectionno == '000':
        messagebox.showinfo('ERROR', 'Section Number must not be 0.')
    elif len(instructorid) != 8:
        messagebox.showinfo('ERROR', 'Instructor must contain 8 characters.')
    else:
        try:
            conn=connection()
            cursor=conn.cursor()
            cursor.execute("INSERT INTO ASSIGN VALUES('"+instructorid+"', '"+sectionno+"', '"+subject+"')",)
            conn.commit()
            conn.close()
            resetAssign()
        except:
            cursor.execute("SELECT INSTRUCTORID FROM INSTRUCTOR WHERE INSTRUCTORID = '"+instructorid+"'")
            instructoridresult = cursor.fetchall()
            cursor.execute("SELECT SECTIONNO FROM SECTION WHERE SECTIONNO = '"+sectionno+"'")
            sectionnoresult = cursor.fetchall()
            if not instructoridresult and not sectionnoresult:
                messagebox.showinfo('ERROR', 'Instructor ID and Section Number are not valid')
            elif not instructoridresult:
                messagebox.showinfo("ERROR", "Instructor ID are not valid")
            elif not sectionnoresult:
                messagebox.showinfo("ERROR", "Section Number are not valid")
            else:
                messagebox.showinfo("ERROR", "Instructor already assigned into the section")
        refreshTableAssign()

def deleteAssign():
    decisionChoices = messagebox.askquestion('Warning!!', 'Do you really want to delete the selected data?')
    if decisionChoices == 'yes':
        try:
            selected = treeAssign.selection()
            deleteitem = []
            j=0
            for record in selected:
                deleteitem.append(treeAssign.item(record, 'values')[0])
                deleteitem.append(treeAssign.item(record, 'values')[1])
                deleteitem.append(treeAssign.item(record, 'values')[2])
           # commandquery = 'DELETE FROM COURSE WHERE COURSEID = %s'
            for i in range(0, len(deleteitem)):
                if j == 0:
                    commandquery = 'DELETE FROM ASSIGN WHERE INSTRUCTORID = "'+deleteitem[i]+'" AND '
                    j += 1
                elif j == 1:
                    commandquery += 'SECTIONNO = '+deleteitem[i]+' AND '
                    j += 1
                else:
                    j = 0
                    commandquery += 'SUBJECT = "'+deleteitem[i]+'"'
                    conn = connection()
                    cursor = conn.cursor()
                    cursor.execute(commandquery)
                    conn.commit()
                    conn.close()
        except:
            messagebox.showinfo('ERROR', "Sorry an error occured!")
            return
    else: return
    refreshTableAssign()

def deleteDataAssign():
    decision = messagebox.askquestion("Warning!!", "Delete all data?")
    if decision != "yes":
        return 
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ASSIGN")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Sorry an error occured")
            return
        refreshTableAssign()

def selectAssign():
    selected = treeAssign.selection()
    if len(selected) == 1:
        for record in selected:
            setAssign1.set(treeAssign.item(record, 'values')[0])
            setAssign2.set(treeAssign.item(record, 'values')[1])
            setAssign3.set(treeAssign.item(record, 'values')[2])
    else: 
        messagebox.showinfo("Error", "Please select only one row")

def searchAssign():
    instructorid=str(txtAInstructorID.get())
    sectionno=str(txtASectionNo.get())
    subject=str(txtASubject.get())

    list=[instructorid, sectionno, subject]
    list2=['instructorid', 'sectionno', 'subject']
    itemsearch = []
    index = []
    command2 = " "

    for i in range(0, 3):
        if bool(list[i]):
            itemsearch.append(list2[i])
            index.append(i)
    
    if len(index) == 0:
        messagebox.showinfo("Error", "Please input in any field to search.")
        return

    for h in range(0, len(index)):
        if(len(index)-1 == h):
            command2 += (list2[index[h]].upper() +"='"+ str(list[index[h]])+"';")
        else:
            command2 += list2[index[h]].upper() +"='"+ str(list[index[h]]) +"' AND " 

    commandquery = 'SELECT * FROM ASSIGN WHERE '
    conn=connection()   
    cursor=conn.cursor()
    cursor.execute(commandquery + command2)
    results=cursor.fetchall()
    conn.close()

    for data in treeAssign.get_children():
        treeAssign.delete(data)
    
    if len(results) == 0:
        readAssign()
        refreshTableAssign()
        messagebox.showinfo("Error", "Data not found")
    else:
        for arr in results:
            treeAssign.insert(parent='', index='end', iid=arr, text='', values=(arr), tag='orow')

def updateAssign():
    selectedAInstructorID = ""
    selectedASectionNo = ""
    try:
        selected_item = treeAssign.selection()[0]
        selectedAInstructorID = str(treeAssign.item(selected_item)['values'][0])
        selectedASectionNo = str(treeAssign.item(selected_item)['values'][1])
    except:
        messagebox.showinfo("Error", "Please select a data row")
        return

    instructorid=str(txtAInstructorID.get())
    sectionno=str(txtASectionNo.get())
    subject=str(txtASubject.get())

    if((instructorid=='' or instructorid==' ') or (sectionno=='' or sectionno==' ') or (subject=='' or subject==' ')):
        messagebox.showinfo('ERROR', 'Please fill up all the blank entry!')
    elif len(instructorid) != 8 and (sectionno == '0' or sectionno == '00' or sectionno == '000'):
        messagebox.showinfo('ERROR', 'Instructor ID must contain 8 characters in the field and the Section Number must not be 0')
    elif sectionno == '0' or sectionno == '00' or sectionno == '000':
        messagebox.showinfo('ERROR', 'Section Number must not be 0.')
    elif len(instructorid) != 8:
        messagebox.showinfo('ERROR', 'Instructor must contain 8 characters.')
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE ASSIGN SET INSTRUCTORID='"+
            instructorid+"', SECTIONNO='"+
            sectionno+"', SUBJECT='"+
            subject+"'WHERE INSTRUCTORID='"+
            selectedAInstructorID+"' AND SECTIONNO="+
            selectedASectionNo+" ")
            conn.commit()
            resetAssign()
        except:
            cursor.execute("SELECT INSTRUCTORID FROM INSTRUCTOR WHERE INSTRUCTORID = '"+instructorid+"'")
            instructoridresult = cursor.fetchall()
            cursor.execute("SELECT SECTIONNO FROM SECTION WHERE SECTIONNO = '"+sectionno+"'")
            sectionnoresult = cursor.fetchall()
            cursor.execute("SELECT INSTRUCTORID FROM ASSIGN WHERE INSTRUCTORID = '"+instructorid+"'")
            assigninsresult = cursor.fetchall()
            cursor.execute("SELECT SECTIONNO FROM ASSIGN WHERE SECTIONNO = '"+sectionno+"'")
            assignsectionnoreult = cursor.fetchall()

            if not instructoridresult and not sectionnoresult:
                messagebox.showinfo('ERROR', 'Instructor ID and Section Number are not valid')
            elif not instructoridresult:
                messagebox.showinfo("ERROR", "Instructor ID are not valid")
            elif assigninsresult and assignsectionnoreult:
                messagebox.showinfo("ERROR", "Instructor ID already have assign subject into section")
            else:
                messagebox.showinfo("ERROR", "Section Number are not valid")
        conn.close()
    refreshTableAssign()

def resetAssign():
    setAssign1.set('')
    setAssign2.set('')
    setAssign3.set('')

    txtAInstructorID.configure(validate="key", validatecommand=idvalid)
    txtASectionNo.configure(validate="key", validatecommand=secvalid)

def resetTableAssign():
    readAssign()
    refreshTableAssign()

fAssign = ctk.CTkFrame(nbTab, width=1280, height=720, bg="#ECECEC")
fAssign.pack()
treeAssign = ttk.Treeview(fAssign, height=13)
treeAssign.place(x=75,y=363)
nbTab.add(fAssign, text='Assign')

lblTitle = Label(fAssign,text='School Management System', background='#2E2E2E', foreground='#11B384', font=('Arial bold', 24))
lblTitle.place(x=440, y=10)

lblAInstructorID = ctk.CTkLabel(fAssign, text='Instructor ID', text_font=('Arial bold', 10), bg='#ECECEC')
lblASectionNo = ctk.CTkLabel(fAssign, text='Section Number', text_font=('Arial bold', 10), bg='#ECECEC')
lblASubject = ctk.CTkLabel(fAssign, text='Subject', text_font=('Arial bold', 10), bg='#ECECEC')

lblAInstructorID.place(x=48, y = 70) 
lblASectionNo.place(x=57, y = 140)
lblASubject.place(x=33, y = 210)

txtAInstructorID = ctk.CTkEntry(fAssign, width=478,text_font=('Arial', 10),textvariable=setAssign1, validate="key", validatecommand=idvalid)
txtASectionNo = ctk.CTkEntry(fAssign, width=478, text_font=('Arial', 10),textvariable=setAssign2, validate="key", validatecommand=secvalid)
txtASubject = ctk.CTkEntry(fAssign, width=478,text_font=('Arial', 10),textvariable=setAssign3)

txtAInstructorID.place(x=78, y=100)
txtASectionNo.place(x=78, y=170)
txtASubject.place(x=78, y=240)

#Setting for the Button Add, Update and Delete
btnAssignAdd = ctk.CTkButton(fAssign,width=100, height=27, text='ADD', text_font=('Arial Bold', 10), command=addAssign)
btnAssignUpdate = ctk.CTkButton(fAssign,width=100, height=27, text='UPDATE', text_font=('Arial Bold', 10), command=updateAssign)
btnAssignDelete = ctk.CTkButton(fAssign,width=100, height=27, text='DELETE', text_font=('Arial Bold', 10), command=deleteAssign)
btnAssignSearch = ctk.CTkButton(fAssign,width=100, height=27, text='SEARCH', text_font=('Arial Bold', 10), command=searchAssign)
btnAssignDeleteAll = ctk.CTkButton(fAssign,width=100, height=27, text='DELETE ALL', text_font=('Arial Bold', 10), command=deleteDataAssign)
btnAssignSelect = ctk.CTkButton(fAssign,width=100, height=27, text='SELECT',  text_font=('Arial Bold', 10), command=selectAssign)
btnAssignReset = ctk.CTkButton(fAssign,width=100, height=27, text='RESET ENTRY',  text_font=('Arial Bold', 10), command=resetAssign)
btnAssignResetTable = ctk.CTkButton(fAssign,width=100, height=27, text='RESET TABLE',  text_font=('Arial Bold', 10), command=resetTableAssign)

btnAssignAdd.place(x=572, y = 102)
btnAssignUpdate.place(x=572, y = 172)
btnAssignDelete.place(x=572, y = 242)
btnAssignSearch.place(x=687, y = 102)
btnAssignDeleteAll.place(x=687, y = 172)
btnAssignSelect.place(x=687, y = 242)
btnAssignReset.place(x=78, y=285)
btnAssignResetTable.place(x=200, y=285)

lblAssignRecords = Label(fAssign,text='Assign Records', background='#2E2E2E', foreground='#11B384', font=('Arial Bold', 20))
lblAssignRecords.place(x=520, y=310)

# Read the Image
image = Image.open("PUP2.jpg")
imgPUP = ImageTk.PhotoImage(image.resize((385, 197)))
 
# create label and add resize image
label1 = ctk.CTkLabel(fAssign,image=imgPUP)   
label1.image = imgPUP
label1.place(x=808, y=72)

treeAssign['columns']=('InstructorID', 'SectionNo', 'Subject')

treeAssign.column('#0', width=0, stretch=NO)
treeAssign.column('InstructorID', anchor=W, width=200)
treeAssign.column('SectionNo', anchor=W, width=200)
treeAssign.column('Subject', anchor=W, width=720)

treeAssign.heading('InstructorID', text='Instructor ID', anchor=W)
treeAssign.heading('SectionNo', text='Section Number', anchor=W)
treeAssign.heading('Subject', text='Subject', anchor=W)

refreshTableAssign()   

root.mainloop()