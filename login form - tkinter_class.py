import tkinter as tk
import tkinter.font as font
from tkinter import *
from tkinter import ttk
#from PIL import ImageTk
import sqlite3
from datetime import datetime
from tkinter import messagebox




#create table in sqlite       
conn = sqlite3.connect('useraccounts.db') #connect to the database
table_create = ''' 
        CREATE TABLE IF NOT EXISTS accounts (
            NAME TEXT,
            USERNAME TEXT,
            PASSWORD TEXT,
            DATE_REGISTERED TEXT )     
    '''

conn.execute(table_create)
conn.commit()
conn.close()



class App(tk.Tk):
    def __init__(self):
        # main window
        super().__init__()

        self.title('Log in Form')
        self.geometry('657x510+350+100')
        self.resizable(False,False)

        self.enterkey = tk.Entry(self)
        

        # widgets
        self.login = Login(self)
            

        # run
        self.mainloop()      

class Menu(ttk.Frame, App):

    # Log in
    def __init__(self, parent):
        super().__init__(parent)

        # Main Frame for the bg
        self.mainframe = Frame(self, height=510, width=657, bg='blue').pack()        
        self.place(x=0, y=0)

        self.mainbg = tk.PhotoImage(file='mainbg.png')
        self.label = tk.Label(self.mainframe, image=self.mainbg).pack()
        self.place(x=0, y=0)


class Login(Menu):   
    def __init__(self, parent):
        super().__init__(parent)                  

        #clear entry fields        
        def clear_logacct(self):    
            self.login_userEntry.delete(0,'end')
            self.login_passEntry.delete(0,'end')

        #ACCESS DATA from DATABASE
        def access_account(self):                 

             self.logemail = self.login_userEntry.get().lower()
             self.logpassword = self.login_passEntry.get()

             #Check Data
             conn = sqlite3.connect('useraccounts.db') #connect to the database

             data_check_query = '''SELECT * FROM accounts WHERE username = (?) AND password = (?)'''
             data_check_tuple = (self.login_userEntry.get(),self.login_passEntry.get())
             print(f"Input: ", data_check_tuple)
             cursor = conn.cursor()
             data = cursor.execute(data_check_query, data_check_tuple) 
             dataget = cursor.fetchone()
             print(f"Database Record: \n", dataget) 


             if dataget:
                print(f"Matched Email:", self.login_userEntry.get(), "\nMatched Password:", self.login_passEntry.get())
                tk.messagebox.showinfo("Log in", "Log in Successful")
                clear_logacct(self)   
                         
             else:
                print(f"Wrong email /password: ", self.login_userEntry.get(), self.login_passEntry.get()) 
                clear_logacct(self)
                tk.messagebox.showerror("Log in", "Invalid Input")
                return False 
                  


             conn.close()
                        

        # Hide and Show Password functionality
        def hide_show_pass():

            if self.login_passEntry['show'] == '●':
                    self.login_passEntry.config(show='') 
                    self.show_btn = Button(self.loginframe,
                            image=self.newhide_btn_img,
                            bg="white",
                            borderwidth=0,
                            activebackground="white",
                            cursor='hand2',
                            command=hide_show_pass)
                    self.show_btn.place(x=228, y=254)      
                    self.show_btn.config(image=self.show_img)

            else:
                    self.login_passEntry.config(show='●')
                    self.newhide_btn = Button(self.loginframe,
                            image=self.show_img,
                            borderwidth=0,
                            bg="white",
                            activebackground="white",
                            cursor='hand2',
                            command=hide_show_pass)
                    self.newhide_btn.place(x=228, y=254)
                    self.newhide_btn.config(image=self.newhide_btn_img) 

        # Login Frame
        self.loginframe = Frame(self.mainframe, height=420, width=275, bg='red')
        self.loginframe.place(x=90, y=45)

        self.loginbg = tk.PhotoImage(file='page1.png')
        self.label = tk.Label(self.loginframe, image=self.loginbg, bg='white').place(x=-6, y=0)
        
        #Log in Button
        self.login_img = tk.PhotoImage(file="login.png")
        self.login_btn = Button(self.loginframe, 
                image=self.login_img,
                borderwidth=0,
                bg="white",
                activebackground="white",
                cursor='hand2',
                command=lambda:access_account(self))        
        self.login_btn.place(x=90, y=320)
        self.login_btn.bind()

        #Sign up Button
        self.login_signupImg = tk.PhotoImage(file="signmember.png")
        self.login_signupBtn = Button(self.loginframe,
                image=self.login_signupImg,
                borderwidth=0,
                bg="white",
                activebackground="white",
                cursor='hand2',
                command=lambda:CreateAccount(self))     
        self.login_signupBtn.place(x=170, y=366)

        #Forgot password Button
        self.login_forgotpass_img = tk.PhotoImage(file="passforgot.png")
        self.login_forgotpassBtn = Button(self.loginframe,
                image=self.login_forgotpass_img,
                borderwidth=0,
                bg="white",
                activebackground="white",
                cursor='hand2',
                command=lambda:ResetPassword(self)
                )
        self.login_forgotpassBtn.place(x=98, y=400)


        #Email textbox
        self.login_userEntry = Entry(self.loginframe,
                #background="yellow",                 
                justify=LEFT,
                borderwidth=0,
                font="{inter} 11 {}",
                foreground="#727272",
                textvariable='self.loguser_var')      
        self.login_userEntry.place(x=29, y=183, width=221, height=24)

        # #Password textbox
        self.login_passEntry = Entry(self.loginframe,
                #background="yellow",
                justify=LEFT,
                borderwidth=0,
                font="{inter} 9 {}",
                foreground="#727272",
                show="●",
                textvariable='self.logpassword_var')    
        self.login_passEntry.place(x=29, y=256, width=180, height=24)


        ###### eye toggle-----------------------------

        #Display ONLY of hide password icon
        self.hide_btn_img = tk.PhotoImage(file="pass_hide.png")
        self.hide_btn = Button(self.loginframe,
                image=self.hide_btn_img,
                borderwidth=0,
                bg="white",
                activebackground="white",
                cursor='hand2',
                command=hide_show_pass)
        self.hide_btn.place(x=228, y=254)


        self.show_img = tk.PhotoImage(file="pass_show.png")
        self.newhide_btn_img = tk.PhotoImage(file="pass_hide.png")   


        self.loguser_var = tk.StringVar()
        self.logpassword_var = tk.StringVar()   
    

class CreateAccount(Login):     
    def __init__(self, parent):       
        super().__init__(parent)
         

        #clear entry fields
        def clear_createacct(self):    
             self.acct_nameEntry.delete(0,'end')
             self.acct_usernameEntry.delete(0,'end')
             self.acct_passEntry.delete(0,'end')

        #INSERT DATA to DATABASE
        def register_account(self):
             #automatic time register
             dateNow = datetime.now()
             dateStr = datetime.strftime(dateNow,'%m-%d-%Y')           

             if self.acct_nameEntry.get() == "" or  self.acct_usernameEntry.get() == "" or self.acct_passEntry.get() == "":

                        messagebox.showerror("Error", "All entries must be filled")
                        clear_createacct(self)
                         

             else:
                        #Insert Data
                        conn = sqlite3.connect('useraccounts.db') #connect to the database
                                  
                        data_insert_query = '''INSERT INTO accounts (name, username, password, date_registered) VALUES 
                        (?, ?, ?, ?)'''
                        data_insert_tuple = (self.acct_nameEntry.get().title(), self.acct_usernameEntry.get(),self.acct_passEntry.get(), dateStr)
                        print(data_insert_tuple)
                        cursor = conn.cursor()
                        cursor.execute(data_insert_query, data_insert_tuple)
                        conn.commit()
                        messagebox.showinfo("Create Account", "New Account Created")
                        conn.close()
                        clear_createacct(self)
                        Login(self)
        
                
        # Create Account Frame
        self.create_acct_frame = Frame(self.mainframe, height=420, width=275)
        self.create_acct_frame.place(x=90, y=45)

        #background of Login Frame
        self.createbg = tk.PhotoImage(file="page2.png")
        self.label= tk.Label(self.create_acct_frame, image=self.createbg, width=275, height=420).place(x=0, y=0)
        
        #Create account Button
        self.createacct_img = tk.PhotoImage(file="create_accbtn.png")
        self.createacct_btn = Button(self.create_acct_frame,
                image=self.createacct_img,
                borderwidth=0,
                bg="white",
                activebackground="white",
                cursor='hand2',
                command=lambda:register_account(self)                               
                )
        self.createacct_btn.place(x=70, y=340)


        #Sign in Button
        self.signin_member_img = tk.PhotoImage(file="signin.png")
        self.signin_member_btn = Button(self.create_acct_frame,
                image=self.signin_member_img,
                borderwidth=0,
                bg="white",
                activebackground="white",
                cursor='hand2',
                command=lambda:Login(self)
                )
        self.signin_member_btn.place(x=160, y=399)


        #Name text box ENTRY
        self.acct_nameEntry = Entry(self.create_acct_frame,
                #background="yellow",
                justify=LEFT,
                borderwidth=0,
                font="{inter} 11 {}",
                foreground="#727272",
                textvariable='self.createname_var')      
        self.acct_nameEntry.place(x=28, y=144, width=221, height=24)

        #Email text box ENTRY
        self.acct_usernameEntry = Entry(self.create_acct_frame,
                #background="yellow",
                borderwidth=0,
                font="{inter} 11 {}",
                foreground="#727272",
                textvariable='self.createuser_var')
        self.acct_usernameEntry.place(x=28, y=210, width=221, height=24)

        #Password textbox
        self.acct_passEntry = Entry(self.create_acct_frame,
                #background="yellow",
                borderwidth=0,
                font="{inter} 11 {}",
                foreground="#727272",
                textvariable='self.createpassword_var')
        self.acct_passEntry.place(x=28, y=285, width=221, height=24)


        self.createname_var = tk.StringVar()
        self.createuser_var = tk.StringVar()
        self.createpassword_var = tk.StringVar()


class ResetPassword(CreateAccount):
    def __init__(self, parent):
        super().__init__(parent)

        #clear entry fields
        def clear_resetacct(self):    
            self.existing_userEntry.delete(0,'end')
            self.new_passEntry.delete(0,'end')
           
        def get_info(self):
           
                if self.existing_userEntry.get() == "" or  self.new_passEntry.get() == "":

                        messagebox.showerror("Error", "All entries must be filled")
                        clear_resetacct(self)                             

                else:     
                        #Check Data
                        conn = sqlite3.connect('useraccounts.db') #connect to the database
                        cursor = conn.cursor()

                        data_query = '''SELECT * FROM accounts WHERE username = (?)'''
                        cursor.execute(data_query,[self.existing_userEntry.get()])                   
                        row = cursor.fetchone()
                        print(f"Database Record: \n", row) 

                        if row == None:
                                messagebox.showerror("Error", "Email not in Database")
                                clear_resetacct(self)
                                ResetPassword(self)
                             

                        else:
                                data_query = '''UPDATE accounts SET password = (?) WHERE username = (?)'''
                                cursor.execute(data_query,[self.new_passEntry.get(), self.existing_userEntry.get()])
                                conn.commit()
                                conn.close()
                                messagebox.showinfo("Reset Password", "Password Changed Successfully")
                                clear_resetacct(self)
                                Login(self)                                       
                      
        #RESET PASSWORD FRAME
        self.reset_frame = Frame(self.mainframe,height=414, width=272, bg='red')
        self.reset_frame.place(x=89, y=45)

        #background of Reset Frame
        self.resetbg = tk.PhotoImage(file="page3.png")
        self.lable = tk.Label(self.reset_frame, image=self.resetbg, width=285, height=427).place(x=-8, y=-1)

        #Update password Button
        self.update_img = tk.PhotoImage(file="update_btn.png")
        self.update_btn = Button(self.reset_frame,
                image=self.update_img,
                borderwidth=0,
                bg="white",
                activebackground="white",
                cursor='hand2',
                command=lambda:get_info(self))
        self.update_btn.place(x=70, y=330)


        #back to sign in Button
        self.sign_img = tk.PhotoImage(file="signin.png")
        self.sign_btn = Button(self.reset_frame,
                image=self.sign_img,
                borderwidth=0,
                bg="white",
                activebackground="white",
                cursor='hand2',
                command=lambda:Login(self))
        self.sign_btn.place(x=120, y=385)



        #Email text box ENTRY
        self.existing_userEntry = Entry(self.reset_frame,
                #background="red",
                justify=LEFT,
                borderwidth=0,
                font="{inter} 11 {}",
                foreground="#727272",
                textvariable='self.existinguser_var')      
        self.existing_userEntry.place(x=32, y=174, width=221, height=24)


        #New password text box ENTRY
        self.new_passEntry = Entry(self.reset_frame,
                #background="yellow",
                justify=LEFT,
                borderwidth=0,
                font="{inter} 11 {}",
                foreground="#727272",
                textvariable='self.newpass_var')      
        self.new_passEntry.place(x=32, y=247, width=221, height=24)


       

        self.existinguser_var = tk.StringVar()
        self.newpass_var = tk.StringVar()
        self.confirmpass_var = tk.StringVar()



App()  
 
 