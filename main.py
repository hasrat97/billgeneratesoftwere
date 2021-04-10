from tkinter import *
import random,os
from tkinter import messagebox,Toplevel,ttk,filedialog
import pymysql

class LoginWin:
    def __init__(self,root):
        self.root = root
        self.root.title("Billing Sofrware - Login Window")
        self.root.resizable(False,False)
        self.root.geometry("1350x710+0+0")

        Background= Label(self.root,bg= "purple")
        Background.place(x=0,y=0,relwidth=1,relheight=1)
        #=== Title ==========
        title = Label(self.root,text="Login System",font=("arial",15,"bold"),bg="purple",fg="white",pady=10,bd=7,relief=GROOVE)
        title.place(x=0,y=0,relwidth=1)

        #========== Variables =============
        self.manageruserVar = StringVar()
        self.managerpassVar = StringVar()


        # ======== Manager Login Form =============
        managerFrame = LabelFrame(self.root,text="Login Area",font=("arial",12,"bold"),fg="gold",bd=5,bg="#115EA6",padx=50)
        managerFrame.place(x=480,y=150,height=400)

        manageruserlbl = Label(managerFrame,text="User name: ",font=("arial",13,"bold"),bg="#115EA6",fg="white").grid(row=1,column=0,padx=10,pady=20,sticky="w")
        managerusertxt = Entry(managerFrame,textvariable=self.manageruserVar,bd=5,relief=SUNKEN,font=("arial",13,"bold")).grid(row=1,column=1,pady=20)

        managerpasslbl = Label(managerFrame,text="Password: ",font=("arial",13,"bold"),bg="#115EA6",fg="white").grid(row=2,column=0,padx=10,pady=10,sticky="w")
        managerpasstxt = Entry(managerFrame,textvariable=self.managerpassVar,bd=5,relief=SUNKEN,font=("arial",13,"bold"),show="*").grid(row=2,column=1,pady=10)

        managerbtn = Button(managerFrame,command=self.Manager_log,text="Login",font=("arial",12,"bold"),width=15,pady=10,bg="black",fg="white").grid(row=3,columnspan=2,pady=15)

    def Manager_log(self):
        if self.manageruserVar.get()=="" or self.managerpassVar.get()=="":
            messagebox.showerror("Error", "All Fields are required")
        else:
            try:
                con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                cur = con.cursor()
                q = "select * from admin where username=%s and password=%s"
                cur.execute(q, (self.manageruserVar.get(), self.managerpassVar.get()))
                row = cur.fetchone()
                if row == "None":
                    messagebox.showerror("Error", "Invalid user name or password.")
                else:
                    self.billingapp()
                    self.manageruserVar.set("")
                    self.managerpassVar.set("")
                    self.root.withdraw()
            except Exception as es:

                messagebox.showerror("Error", f"Error due to: {str(es)}")

    def billingapp(self):
        self.billroot = Toplevel()
        self.billroot.grab_set()
        self.billroot.title("Billing Software")
        self.billroot.resizable(False,False)
        self.billroot.geometry("1350x710+0+0")

        #========= Variables ===================
        global admin
        con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
        cur = con.cursor()
        q = "select * from admin where username=%s"
        cur.execute(q,(self.manageruserVar.get()))
        rows = cur.fetchall()
        for row in rows:
            adminname = [row[0], row[1], row[2]]
            username = adminname[0]
            admin = adminname[2]

        # ============ customer Info Var ============

        self.CnameVar = StringVar()
        self.CphoneVar = StringVar()
        self.billnoVar = StringVar()

        r_bill = random.randint(1000, 9999)
        self.billnoVar.set(r_bill)

        self.billsearchVar = StringVar()

        # ============ Products Form Var ============
        self.Qty1Var = IntVar()
        self.Qty2Var = IntVar()
        self.Qty3Var = IntVar()
        self.Qty4Var = IntVar()
        self.Qty5Var = IntVar()

        headertitle = Label(self.billroot, text="Billing System", bg="purple", fg="white", font=("arial", 20, "bold"),pady=10, bd=7, relief=GROOVE)
        headertitle.place(x=0, y=0, relwidth=1)
        # ============ Customer information Frame ===================
        CFrame = LabelFrame(self.billroot, text="Customer Information", font=("arial", 10, "bold"), fg="gold", bd=5,bg="purple")
        CFrame.place(x=0, y=65, relwidth=1)

        # ========= Rure Button =============
        userrule = Label(self.billroot, text="Rule: " + admin, font=("arial", 12, "bold"), bg="purple", fg="white")
        userrule.place(x=10, y=15)

        # ============ Customer information Form ===================
        CNamelbl = Label(CFrame, text="Customer Name: ", font=("arial", 12, "bold"), bg="purple", fg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        CnameEntry = Entry(CFrame, textvariable=self.CnameVar, width=20, font=("arial", 12, "bold"), bd=7,relief=SUNKEN).grid(row=0, column=1, padx=10, pady=5)

        CPhoelbl = Label(CFrame, text="Phone Number: ", font=("arial", 12, "bold"), bg="purple", fg="white").grid(row=0,column=2, padx=10, pady=5, sticky="w")
        CPhoneEntry = Entry(CFrame, textvariable=self.CphoneVar, width=20, font=("arial", 12, "bold"), bd=7,relief=SUNKEN).grid(row=0, column=3, padx=10, pady=5)

        billnumber = Label(CFrame, text="Bill Number: ", font=("arial", 12, "bold"), bg="purple", fg="white").grid(row=0, column=4, padx=10, pady=5, sticky="w")
        billnumberEntry = Entry(CFrame, textvariable=self.billsearchVar, width=20, font=("arial", 12, "bold"), bd=7,relief=SUNKEN).grid(row=0, column=5, padx=10, pady=5)

        billsearchbtn = Button(CFrame, command=self.search_bill, text="Search Bill", font=("arial", 12, "bold"),bg="skyblue", fg="#222222").grid(row=0, column=6, padx=10, pady=5)

        #============================= Products Frame ===================================

        ProFrame = LabelFrame(self.billroot,text="Product Section",fg="gold",bd=7,relief=GROOVE,bg="purple",font=("arial", 10,"bold"))
        ProFrame.place(x=0,y=133,width=800,height=450)

        global pro1price

        con = pymysql.connect(host="localhost",user="root",password="root1234",database="billdata")
        cur = con.cursor()
        q = "select title from product"
        cur.execute(q)
        rows = cur.fetchall()
        self.ProductList = list()
        for row in rows:
            for i in row:
                self.ProductList.append(i)

        # ================ Billing Frame ==================
        BillFrame = Frame(self.billroot, bd=7, relief=GROOVE)
        BillFrame.place(x=800, y=133, height=450, width=550)

        bill_title = Label(BillFrame, text="Billing Area", bd=5, relief=GROOVE, font=("arial", 12, "bold"),pady=5)
        bill_title.pack(side=TOP, fill=X)
        scroll_y = Scrollbar(BillFrame, orient=VERTICAL)
        self.txtarea = Text(BillFrame, yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.txtarea.yview)
        self.txtarea.pack(fill=BOTH, expand=1)


root = Tk()
obj = LoginWin(root)
root.mainloop()



