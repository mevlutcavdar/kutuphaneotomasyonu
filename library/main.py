#Gerekli pencere ve kütüphanelerin çekilmesi
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from main_window import*
from officer_window import*
from User_window import*
import sqlite3
import time
from datetime import date

#giriş sayfası için bağlantılar
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

#user sayfası için bağlantılar
app2 = QtWidgets.QApplication(sys.argv)
MainWindow2 = QtWidgets.QMainWindow()
ui2 = Ui_user_window()
ui2.setupUi(MainWindow2)

#officer sayfası için bağlantılar
app3 = QtWidgets.QApplication(sys.argv)
MainWindow3 = QtWidgets.QMainWindow()
ui3 = Ui_officer_window()
ui3.setupUi(MainWindow3)

#ilk giriş sayfası açılacak
MainWindow.show()

global curs
global conn

def login():
    conn = sqlite3.connect("library.db")
    curs = conn.cursor()

    id = ui.lneuserid.text()
    password =ui.lnepassword.text()
    # print(id,password)

    curs.execute("Select * From user")
    data = curs.fetchall()
    # print(data)

    for i in data:
        if id == str(i[0]) and password == str(i[3]):
            if i[4] == "u":
                def book_on_me ():
                    conn = sqlite3.connect("library.db")
                    curs = conn.cursor()     
                    user_id=ui.lneuserid.text()
                    current_date = time.strftime("%y.%m.%d",time.localtime())
                    book_on = []
                    total_day=[]
                    curs.execute("Select book_id,rent_date,retrieve_date From rent_retrieve WHERE user_id='%s' AND retrieve_date=''"%(user_id))
                    data1 = curs.fetchall() 
                    # print(data1)
                    for i in data1 :
                        curs.execute("SELECT book_id,book_name,category,author,publisher,book_price,about FROM book \
                            WHERE book_id=? ",(int(i[0]),))
                        data_book=curs.fetchall()
                        book_on.append(data_book[0])
                    for i in data1 :
                        a=date(int(current_date[:2]),int(current_date[3:5]),int(current_date[6:8]))
                        b=date(int(i[1][:2]),int(i[1][3:5]),int(i[1][6:8]))                    
                        day=(a-b).days
                        if day > 30:
                            punishment = (day/30)*1
                        else:
                            punishment=0                   
                        curs.execute("UPDATE rent_retrieve SET punishment = ? WHERE book_id = ? AND retrieve_date =''"\
                            ,(int(punishment),int(data1[0][0])))
                        conn.commit()    
                        total_day.append(day)
                    # print(data1)                       
                    total_day=tuple(total_day)
                    for i in range(len(book_on)):
                        book_on[i]+=(total_day[i],)
                    print(book_on)
                    ui2.tblbom.insertRow(0)
                    for row , rowdata in enumerate(book_on):
                        for column, columndata in enumerate(rowdata):
                            ui2.tblbom.setItem(row,column,QTableWidgetItem(str(columndata)))
                            column+=1

                        row_position = ui2.tblbom.rowCount()
                        ui2.tblbom.insertRow(row_position)             

                def book_read ():
                    conn = sqlite3.connect("library.db")
                    curs = conn.cursor()     
                    user_id=ui.lneuserid.text()
                    book_read = []
                    curs.execute("Select book_id,retrieve_date From rent_retrieve WHERE user_id='%s' AND retrieve_date<>''"%(user_id))
                    data2 = curs.fetchall() 
                    for i in data2 :
                        curs.execute("SELECT book_id,book_name,category,author,publisher,book_price,about FROM book \
                            WHERE book_id=? ",(int(i[0]),))
                        data_book2=curs.fetchall()
                        book_read.append(data_book2[0])

                    for i in range(len(book_read)):
                        book_read[i]+=(data2[i][1],)
                    ui2.tblbiar.insertRow(0)
                    for row , rowdata in enumerate(book_read):
                        for column, columndata in enumerate(rowdata):
                            ui2.tblbiar.setItem(row,column,QTableWidgetItem(str(columndata)))
                            column+=1

                        row_position = ui2.tblbiar.rowCount()
                        ui2.tblbiar.insertRow(row_position)          
                def punishment():
                    conn = sqlite3.connect("library.db")
                    curs = conn.cursor()     
                    user_id=ui.lneuserid.text()
                    current_date = time.strftime("%y.%m.%d",time.localtime())
                    punishment = []
                    total_day=[]
                    curs.execute("Select book_id,rent_date,retrieve_date,punishment From rent_retrieve WHERE user_id='%s' AND retrieve_date=''"%(user_id))
                    data1 = curs.fetchall() 
                    for i in data1 :
                        curs.execute("SELECT rent_retrieve.book_id,book.book_name,rent_retrieve.punishment FROM book,rent_retrieve\
                             WHERE rent_retrieve.book_id=book.book_id AND book.book_id = ? AND rent_retrieve.user_id=? ",(int(i[0]),int(user_id),))
                        data_book=curs.fetchall()
                        punishment.append(data_book[0])
                    for i in data1 :
                        a=date(int(current_date[:2]),int(current_date[3:5]),int(current_date[6:8]))
                        b=date(int(i[1][:2]),int(i[1][3:5]),int(i[1][6:8]))                    
                        day=((a-b).days)
                        total_day.append(day)
                    for i in range(len(punishment)):
                        punishment[i]+=(total_day[i],)
                    print(punishment)
                    ui2.tblp.insertRow(0)
                    for row , rowdata in enumerate(punishment):
                        print(rowdata)
                        for column, columndata in enumerate(rowdata):
                            print(columndata)
                            ui2.tblp.setItem(row,column,QTableWidgetItem(str(columndata)))
                            column+=1

                        row_position = ui2.tblp.rowCount()
                        ui2.tblp.insertRow(row_position)             


                punishment()
                book_on_me()
                book_read()
                MainWindow.close()
                MainWindow2.show()
            elif i[4] == "o":
                conn = sqlite3.connect("library.db")
                curs = conn.cursor() 
                MainWindow.close()     
                MainWindow3.show()
        else:
            ui.statusbar.showMessage("Username Or Password İs İncorrect !!!",10000)

def search():
    conn = sqlite3.connect("library.db")
    curs = conn.cursor()   

    word = ui.lnesearch.text() 
    # print(word)

    curs.execute("Select * From book")
    data = curs.fetchall()
    # print(word)

    new_data = []
    for i in data:
        for j in i :
            if word in str(j):
                new_data.append(i)
                break
    # print(new_data)
    ui.tblbook.insertRow(0)
    for row , rowdata in enumerate(new_data):
        for column, columndata in enumerate(rowdata):
            ui.tblbook.setItem(row,column,QTableWidgetItem(str(columndata)))
            column+=1

        row_position = ui.tblbook.rowCount()
        ui.tblbook.insertRow(row_position)

def save11():
    conn = sqlite3.connect("library.db")
    curs = conn.cursor()       

    book_id = ui3.lne11bookid.text()
    book_name = ui3.lne11bookname.text()
    category = ui3.lne11category.text()
    author = ui3.lne11author.text()
    publisher = ui3.lne11publisher.text()
    book_price = ui3.lne11bookprice.text()
    about=ui3.lne11about.text()

    adduser = QMessageBox.question(MainWindow,"Add A New Book", "Are You Sure You Want To Add A New Book?", 
    QMessageBox.Yes | QMessageBox.No)

    if adduser == QMessageBox.Yes:

        try:
            curs.execute("INSERT INTO book VALUES (?,?,?,?,?,?,?)" ,\
                (int(book_id),book_name,category,author \
                ,publisher,int(book_price),about,) )
            conn.commit()
            ui3.statusbar.showMessage("Book Successfully Added")
            ui3.lne11bookid.clear()
            ui3.lne11bookname.clear()
            ui3.lne11category.clear()
            ui3.lne11author.clear()
            ui3.lne11publisher.clear()
            ui3.lne11bookprice.clear()
            
        except Exception as error :
            ui3.statusbar.showMessage("An Error Occurred While Adding The Book === "+str(error))

    else:
        ui3.statusbar.showMessage("Adding The Book Has Been Cancelled.")

    # curs.execute("INSERT INTO book VALUES (?,?,?,?,?,?,?)" ,\
    #      (int(book_id),book_name,category,author \
    #     ,publisher,int(book_price),about,) )

    # conn.commit()

def search12():
    conn = sqlite3.connect("library.db")
    curs = conn.cursor()   
    id = ui3.lne12searchid.text() 
    # print(id)
    curs.execute("Select * From book WHERE book_id='%s'"%(id))
    data = curs.fetchall()
    # print(data)

    new_data = []

    for i in data:
        for j in i :
            if id in str(j):
                new_data.append(i)
                break
    
    # print(new_data)

    ui3.lne12bookid.setText(str(new_data[0][0]))
    ui3.lne12bookname.setText(str(new_data[0][1]))
    ui3.lne12category.setText(str(new_data[0][2]))
    ui3.lne12author.setText(str(new_data[0][3]))
    ui3.lne12publisher.setText(str(new_data[0][4]))
    ui3.lne12bookprice.setText(str(new_data[0][5]))
    ui3.lne12about.setText(str(new_data[0][6]))

def delete12():
    conn = sqlite3.connect("library.db")
    curs = conn.cursor()   
    id=ui3.lne12searchid.text()
    delete=QMessageBox.question(MainWindow,"Delete The Book","Are You Sure You Want To Delete The Book ?",\
                         QMessageBox.Yes | QMessageBox.No)
    if delete==QMessageBox.Yes:
        try:
            curs.execute("DELETE FROM book WHERE book_id='%s'" %(id))
            conn.commit()
                        
            ui3.statusbar.showMessage("Book Successfully Deleted",10000)
        except Exception as Hata:
            ui3.statusbar.showMessage("An Error Occurred While Deleting The Book:"+str(Hata))
    else:
        ui3.statusbar.showMessage("Deleting The Book Has Been Cancelled.",10000)

    ui3.lne11bookid.clear()
    ui3.lne11bookname.clear()
    ui3.lne11category.clear()
    ui3.lne11author.clear()
    ui3.lne11publisher.clear()
    ui3.lne11bookprice.clear()           

def save12 ():

    conn = sqlite3.connect("library.db")
    curs = conn.cursor()       

    book_id = ui3.lne12bookid.text()
    book_name = ui3.lne12bookname.text()
    category = ui3.lne12category.text()
    author = ui3.lne12author.text()
    publisher = ui3.lne12publisher.text()
    book_price = ui3.lne12bookprice.text()
    about=ui3.lne12about.text()   
    


    save=QMessageBox.question(MainWindow,"Edit The Book","Are You Sure You Want To Update The Book ?",\
                         QMessageBox.Yes | QMessageBox.No)
    if save==QMessageBox.Yes:
        try:
            curs.execute("UPDATE book SET book_name=?, category=?,\
                author=?, publisher=?, book_price=?, about=? WHERE book_id=?", \
                                (book_name,category,author,publisher,\
                                    book_price,about,book_id))
            conn.commit()                      
            ui3.statusbar.showMessage("Book Successfully Updated",10000)
        except Exception as Hata:
            ui3.statusbar.showMessage("An Error Occurred While Updating The Book:"+str(Hata))
    else:
        ui3.statusbar.showMessage("Updating The Book Has Been Cancelled.",10000)

def adduser():
    conn = sqlite3.connect("library.db")
    curs = conn.cursor()       

    user_id = ui3.lne31userid.text()
    user_name = ui3.lne31username.text()
    mail_adress = ui3.lne31email.text()
    password = ui3.lne31password.text()
    passwordagain = ui3.lne31passwordagain.text()

    if password!=passwordagain :
        ui3.statusbar.showMessage("Password Are Not Same",1000)
    else:
        if ui3.rbtn31user.isChecked() == True:
            curs.execute("INSERT INTO user VALUES (?,?,?,?,?)" ,\
            (int(user_id ),user_name,mail_adress,password \
            ,"u",) )
            conn.commit()   
            ui3.statusbar.showMessage("User Registration Successful",1000)
            ui3.lne31userid.clear()
            ui3.lne31username.clear()
            ui3.lne31email.clear()
            ui3.lne31password.clear()
            ui3.lne31passwordagain.clear()
            ui3.rbtn31officer.setChecked(False)
            ui3.rbtn31user.setChecked(False)

        elif ui3.rbtn31officer.isChecked() == True:        
            curs.execute("INSERT INTO user VALUES (?,?,?,?,?)" ,\
            (int(user_id),user_name,mail_adress,password \
            ,"o",) )
            conn.commit()              
            ui3.statusbar.showMessage("Officer Registration Successful",1000)
            ui3.lne31userid.clear()
            ui3.lne31username.clear()
            ui3.lne31email.clear()
            ui3.lne31password.clear()
            ui3.lne31passwordagain.clear()
            ui3.rbtn31officer.setChecked(False)
            ui3.rbtn31user.setChecked(False)            
        else:
            ui3.statusbar.showMessage("Please Select A Button",1000)
            

def login32() :

    conn = sqlite3.connect("library.db")
    curs = conn.cursor()   
    id = ui3.lne32useridlogin.text() 
    # print(id)
    curs.execute("Select * From user WHERE user_id='%s'"%(id))
    data = curs.fetchall()
    # print(data)

    new_data = []

    for i in data:
        for j in i :
            if id in str(j):
                new_data.append(i)
                break
    
    print(new_data)

    ui3.lne32userid.setText(str(new_data[0][0]))
    ui3.lne32username.setText(str(new_data[0][1]))
    ui3.lne32email.setText(str(new_data[0][2]))
    ui3.lne32password.setText(str(new_data[0][3]))

    # conn = sqlite3.connect("library.db")
    # curs = conn.cursor()

    # id = ui3.lne32useridlogin.text()
    # password =ui3.lne32passwordlogin.text()

    # curs.execute("Select * From user")
    # data = curs.fetchall()

    # for i in data:
    #     if id == str(i[0]) and password == str(i[3]):
    #         if i[4] == "u":
    #             MainWindow3.close()
    #             MainWindow2.show()
    #         else:
    #             pass

def delete32():
    conn = sqlite3.connect("library.db")
    curs = conn.cursor()   
    id=ui3.lne32userid.text()
    cevap=QMessageBox.question(MainWindow,"Delete The User","Are You Sure You Want To Delete The User ?",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        try:
            curs.execute("DELETE FROM user WHERE user_id='%s'" %(id))
            conn.commit()
            ui3.statusbar.showMessage("User Successfully Deleted",10000)
        except Exception as Hata:
            ui3.statusbar.showMessage("An Error Occurred While Deleting The User:"+str(Hata))
    else:
        ui3.statusbar.showMessage("Deleting The User Has Been Cancelled.",10000)
                
def save32 ():

    conn = sqlite3.connect("library.db")
    curs = conn.cursor()       

    user_id = ui3.lne32userid.text()
    user_name = ui3.lne32username.text()
    mail_adress = ui3.lne32email.text()
    password = ui3.lne32password.text()
    
    if ui3.rbtn32user.isChecked() == True:
        curs.execute("UPDATE user SET user_name=?, mail_adress=?,\
            password=? ,type=? WHERE user_id=?", \
                            (user_name,mail_adress,\
                                password,"u",user_id))
        conn.commit()   
        ui3.statusbar.showMessage("User Edit Successful",1000)
        ui3.lne32userid.clear()
        ui3.lne32username.clear()
        ui3.lne32email.clear()
        ui3.lne32password.clear()
        ui3.rbtn32officer.setChecked(False)
        ui3.rbtn32user.setChecked(False)

    elif ui3.rbtn32officer.isChecked() == True:        
        curs.execute("UPDATE user SET user_name=?, mail_adress=?,\
            password=? ,type=? WHERE user_id=?", \
                            (user_name,mail_adress,\
                                password,"o",user_id))
        conn.commit()              
        ui3.statusbar.showMessage("Officer Registration Successful",1000)
        ui3.lne32userid.clear()
        ui3.lne32username.clear()
        ui3.lne32email.clear()
        ui3.lne32password.clear()
        ui3.rbtn32officer.setChecked(False)
        ui3.rbtn32user.setChecked(False)           
    else:
        ui3.statusbar.showMessage("Please Select A Button",1000)

    # curs.execute("UPDATE user SET user_name=?, mail_adress=?,\
    #      password=?,type=? WHERE user_id=?", \
    #                      (user_name,mail_adress,password,publisher,\
    #                         book_price,about,user_id))
    # conn.commit()


def search22():
    conn = sqlite3.connect("library.db")
    curs = conn.cursor()   
    id = ui3.lne22bookid.text() 
    # print(id)
    curs.execute("Select * From book WHERE book_id='%s'"%(id))
    data = curs.fetchall()
    print(data)

    new_data = []

    for i in data:
        for j in i :
            if id in str(j):
                new_data.append(i)
                break
    
    print(new_data)
    ui3.lne22bookname.setText(str(new_data[0][1]))


def rent_rent():
    conn = sqlite3.connect("library.db")
    curs = conn.cursor()   

    book_id = ui3.lne22bookid.text()
    user_id = ui3.lne22userid.text()

    rent_date = time.strftime("%y.%m.%d",time.localtime())
    print(rent_date)
    curs.execute("INSERT INTO rent_retrieve VALUES (?,?,?,?,?) ",(int(book_id),int(user_id),rent_date,"",0))
    conn.commit()
    ui3.statusbar.showMessage("Successfully Book İs Rent")
    ui3.lne22bookid.clear()
    ui3.lne22userid.clear()
    ui3.lne22bookname.clear()


def search23():
    conn = sqlite3.connect("library.db")
    curs = conn.cursor()   
    id = ui3.lne23bookid.text() 
    # print(id)
    curs.execute("Select * From book WHERE book_id='%s'"%(id))
    data = curs.fetchall()
    # print(data)

    new_data = []

    for i in data:
        for j in i :
            if id in str(j):
                new_data.append(i)
                break
    
    # print(new_data)
    ui3.lne23bookname.setText(str(new_data[0][1]))


def retrieve23():
    conn = sqlite3.connect("library.db")
    curs = conn.cursor()   

    book_id = ui3.lne23bookid.text()
    user_id = ui3.lne23userid.text()
    retrieve_date = time.strftime("%y.%m.%d",time.localtime())

    curs.execute("SELECT rent_date FROM rent_retrieve WHERE book_id=? AND retrieve_date=''",(int(book_id),))
    rent_date = curs.fetchall()
    # print(rent_date[0][0][:2])
    # print(retrieve_date[:2])

    a=date(int(retrieve_date[:2]),int(retrieve_date[3:5]),int(retrieve_date[6:8]))
    b=date(int(rent_date[0][0][:2]),int(rent_date[0][0][3:5]),int(rent_date[0][0][6:8]))
    # print(a)
    # print(b)
    day=(a-b).days
    if day > 30:
        punishment = (day/30)*1
    else:
        punishment=0

    curs.execute("UPDATE rent_retrieve SET retrieve_date = ? , punishment = ? WHERE book_id = ? AND retrieve_date =''"\
        ,(retrieve_date,int(punishment),int(book_id)))
    conn.commit()
    ui3.statusbar.showMessage("Successfully Book İs Retrieve")
    ui3.lne23bookid.clear()
    ui3.lne23userid.clear()
    ui3.lne23bookname.clear()

def search21 ():
    conn = sqlite3.connect("library.db")
    curs = conn.cursor()     
    book_id=ui3.lne21search.text()
    current_date = time.strftime("%y.%m.%d",time.localtime())
    curs.execute("Select * From rent_retrieve WHERE book_id='%s'"%(book_id))
    data = curs.fetchall() 
    user_id=data[0][1]   
    retrieve_date = data[0][3]
    # print(data[0][3])        
    
    if (len(retrieve_date)==0):
        curs.execute("Select * From user,book,rent_retrieve WHERE rent_retrieve.book_id='%s' AND user.user_id='%s' AND book.book_id='%s'"%(book_id,user_id,book_id))
        data1 = curs.fetchall()
        rent_date = []
        rent_date.append(data1[0][14])        
        # print(rent_date) 
        # print(current_date)
        a=date(int(current_date[:2]),int(current_date[3:5]),int(current_date[6:8]))
        b=date(int(rent_date[0][:2]),int(rent_date[0][3:5]),int(rent_date[0][6:8]))
        day=(a-b).days
        if day > 30:
            punishment = (day/30)*1
        else:
            punishment=0    
        list = [[int(book_id),(data1[0][6]),(data1[0][1]),int(day),int(punishment)]]
        # print(list)

        ui3.tbl21materialcondition.insertRow(0)
        for row , rowdata in enumerate(list):
            for column, columndata in enumerate(rowdata):
                ui3.tbl21materialcondition.setItem(row,column,QTableWidgetItem(str(columndata)))
                column+=1

            row_position = ui3.tbl21materialcondition.rowCount()
            ui3.tbl21materialcondition.insertRow(row_position)    
    else:
        ui3.statusbar.showMessage("you can take this book")
        print()


ui.btnlogin.clicked.connect(login)
ui.btnsearch.clicked.connect(search)
ui3.btn11save.clicked.connect(save11)

ui3.btn12searchid.clicked.connect(search12)
ui3.btn12delete.clicked.connect(delete12)
ui3.btn12save.clicked.connect(save12)
ui3.btn31adduser.clicked.connect(adduser)
ui3.btn32login.clicked.connect(login32)
ui3.btn32delete.clicked.connect(delete32)
ui3.btn32save.clicked.connect(save32)
ui3.btn22search.clicked.connect(search22)
ui3.btn22rent.clicked.connect(rent_rent)
ui3.btn23search.clicked.connect(search23)
ui3.btn23rent.clicked.connect(retrieve23)
ui3.btn21search.clicked.connect(search21)
sys.exit(app.exec_())

