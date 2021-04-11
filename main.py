from tkinter import *
import random,os
from tkinter import messagebox,Toplevel,ttk,filedialog
import pymysql
import time,tempfile
import pandas

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
        self.Qty6Var = IntVar()
        self.Qty7Var = IntVar()
        self.Qty8Var = IntVar()
        self.Qty9Var = IntVar()
        self.Qty10Var = IntVar()

        # ============ Bottom Form Var ============
        self.totalVar = StringVar()
        self.DisVar = IntVar()
        self.netTotalVar = StringVar()
        self.CpayVar = IntVar()
        self.CreturenVar = StringVar()

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

        self.ProductOne = StringVar()
        self.ProductOne.set("--Select One--")

        self.ProductTwo = StringVar()
        self.ProductTwo.set("--Select One--")

        self.ProductThree = StringVar()
        self.ProductThree.set("--Select One--")

        self.ProductFour = StringVar()
        self.ProductFour.set("--Select One--")

        self.ProductFive = StringVar()
        self.ProductFive.set("--Select One--")

        self.ProductSix = StringVar()
        self.ProductSix.set("--Select One--")

        self.ProductSeven = StringVar()
        self.ProductSeven.set("--Select One--")

        self.ProductEight = StringVar()
        self.ProductEight.set("--Select One--")

        self.ProductNine = StringVar()
        self.ProductNine.set("--Select One--")

        self.ProductTen = StringVar()
        self.ProductTen.set("--Select One--")

        pro1 = OptionMenu(ProFrame, self.ProductOne, *self.ProductList)
        pro1.grid(row=0, column=0, pady=10, padx=10, sticky="w")
        pro1.config(width=12, font=("arail", 10, "bold"))
        pro1qtyEntry = Entry(ProFrame, textvariable=self.Qty1Var, width=10, font=("arial", 10, "bold"), bd=5,relief=SUNKEN).grid(row=0, column=1, pady=10, padx=10)

        pro2 = OptionMenu(ProFrame, self.ProductTwo, *self.ProductList)
        pro2.grid(row=1, column=0, pady=10, padx=10, sticky="w")
        pro2.config(width=12, font=("arail", 10, "bold"))
        pro2Entry = Entry(ProFrame, textvariable=self.Qty2Var, width=10, font=("arial", 10, "bold"), bd=5,relief=SUNKEN).grid(row=1, column=1, pady=10, padx=10)

        pro3 = OptionMenu(ProFrame, self.ProductThree, *self.ProductList)
        pro3.grid(row=2, column=0, pady=10, padx=10, sticky="w")
        pro3.config(width=12, font=("arail", 10, "bold"))
        pro3Entry = Entry(ProFrame, textvariable=self.Qty3Var, width=10, font=("arial", 10, "bold"), bd=5,relief=SUNKEN).grid(row=2, column=1, pady=10, padx=10)

        pro4 = OptionMenu(ProFrame, self.ProductFour, *self.ProductList)
        pro4.grid(row=3, column=0, pady=10, padx=10, sticky="w")
        pro4.config(width=12, font=("arail", 10, "bold"))
        pro4Entry = Entry(ProFrame, textvariable=self.Qty4Var, width=10, font=("arial", 10, "bold"), bd=5,relief=SUNKEN).grid(row=3, column=1, pady=10, padx=10)

        pro5 = OptionMenu(ProFrame, self.ProductFive, *self.ProductList)
        pro5.grid(row=4, column=0, pady=10, padx=10, sticky="w")
        pro5.config(width=12, font=("arail", 10, "bold"))
        pro5Entry = Entry(ProFrame, textvariable=self.Qty5Var, width=10, font=("arial", 10, "bold"), bd=5,relief=SUNKEN).grid(row=4, column=1, pady=10, padx=10)

        pro6 = OptionMenu(ProFrame, self.ProductSix, *self.ProductList)
        pro6.grid(row=5, column=0, pady=10, padx=10, sticky="w")
        pro6.config(width=12, font=("arail", 10, "bold"))
        pro6Entry = Entry(ProFrame, textvariable=self.Qty6Var, width=10, font=("arial", 10, "bold"), bd=5,relief=SUNKEN).grid(row=5, column=1, pady=10, padx=10)

        pro7 = OptionMenu(ProFrame, self.ProductSeven, *self.ProductList)
        pro7.grid(row=6, column=0, pady=10, padx=10, sticky="w")
        pro7.config(width=12, font=("arail", 10, "bold"))
        pro7Entry = Entry(ProFrame, textvariable=self.Qty7Var, width=10, font=("arial", 10, "bold"), bd=5,relief=SUNKEN).grid(row=6, column=1, pady=10, padx=10)

        pro8 = OptionMenu(ProFrame, self.ProductEight, *self.ProductList)
        pro8.grid(row=7, column=0, pady=10, padx=10, sticky="w")
        pro8.config(width=12, font=("arail", 10, "bold"))
        pro8Entry = Entry(ProFrame, textvariable=self.Qty8Var, width=10, font=("arial", 10, "bold"), bd=5,relief=SUNKEN).grid(row=7, column=1, pady=10, padx=10)

        pro9 = OptionMenu(ProFrame, self.ProductNine, *self.ProductList)
        pro9.grid(row=0, column=2, pady=10, padx=15, sticky="w")
        pro9.config(width=12, font=("arail", 10, "bold"))
        pro9Entry = Entry(ProFrame, textvariable=self.Qty9Var, width=10, font=("arial", 10, "bold"), bd=5,relief=SUNKEN).grid(row=0, column=3, pady=10, padx=15)

        pro10 = OptionMenu(ProFrame, self.ProductTen, *self.ProductList)
        pro10.grid(row=1, column=2, pady=10, padx=15, sticky="w")
        pro10.config(width=12, font=("arail", 10, "bold"))
        pro10Entry = Entry(ProFrame, textvariable=self.Qty10Var, width=10, font=("arial", 10, "bold"), bd=5,relief=SUNKEN).grid(row=1, column=3, pady=10, padx=15)



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

        self.welcomebill()
        if admin == "Admin":
            ConFrame = LabelFrame(ProFrame, text="Control Backend", font=("arial", 12, "bold"), fg="gold", bd=7,relief=GROOVE)
            ConFrame.place(x=300, y=300, width=430, height=120)
            addtbtn = Button(ConFrame, command=self.AddPro, text="Add Product", font=("arial", 10, "bold"), bg="purple",fg="white", pady=5, bd=7, activebackground="black", activeforeground="white").grid(row=0,column=0,pady=15,padx=5)
            salesreportbtn = Button(ConFrame, command=self.rewin, text="View Report", font=("arial", 10, "bold"),bg="purple", fg="white", pady=5, bd=7, activebackground="black",activeforeground="white").grid(row=0, column=1, pady=15, padx=5)
            addusertbtn = Button(ConFrame, command=self.AddUser, text="Add User", font=("arial", 10, "bold"),bg="purple", fg="white", pady=5, bd=7, activebackground="black",activeforeground="white").grid(row=0, column=2, pady=15, padx=5)

        #=======Calculation Frame=============

        BottomFrame = LabelFrame(self.billroot, text="Calculation Area", bd=7, relief=GROOVE, fg="gold",font=("arial", 10, "bold"), bg="purple")
        BottomFrame.place(x=0, relwidth=1, height=125, y=583)

        Totallbl = Label(BottomFrame, text="Total Bill: ", font=("arail", 10, "bold"), bg="purple", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        TotalEntry = Entry(BottomFrame, textvariable=self.totalVar, width=10, bd=5, relief=SUNKEN,font=("arail", 10, "bold")).grid(row=0, column=1, pady=5, padx=5)

        Discountlbl = Label(BottomFrame, text="Discount: ", font=("arail", 10, "bold"), bg="purple", fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        DiscountEntry = Entry(BottomFrame, textvariable=self.DisVar, width=10, bd=5, relief=SUNKEN,font=("arail", 10, "bold")).grid(row=1, column=1, pady=5, padx=5)

        NetTotallbl = Label(BottomFrame, text="Net Total: ", font=("arail", 12, "bold"), bg="purple", fg="white").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        NetTotalEntry = Entry(BottomFrame, textvariable=self.netTotalVar, width=10, bd=5, relief=SUNKEN,font=("arail", 12, "bold"), bg="red", fg="white").grid(row=0, column=3, pady=5, padx=5)

        CPaylbl = Label(BottomFrame, text="Customer Pay: ", font=("arail", 10, "bold"), bg="purple", fg="white").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        CPayEntry = Entry(BottomFrame, textvariable=self.CpayVar, width=10, bd=5, relief=SUNKEN,font=("arail", 12, "bold")).grid(row=1, column=3, pady=5, padx=5)

        CReturnlbl = Label(BottomFrame, text="Customer Return: ", font=("arail", 12, "bold"), bg="purple",fg="white").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        CReturnEntry = Entry(BottomFrame, textvariable=self.CreturenVar, width=10, bd=5, relief=SUNKEN,font=("arail", 12, "bold"), bg="skyblue", fg="red").grid(row=0, column=5, pady=5, padx=5)
        #==========Button frame===============

        BtnFrame = Frame(BottomFrame, bd=7, relief=GROOVE)
        BtnFrame.place(x=680, width=650, height=95)

        Totalbtn = Button(BtnFrame, command=self.total_sum, text="Total", font=("arial", 12, "bold"), bg="purple",fg="white", pady=10, width=10, bd=7, activebackground="black", activeforeground="white").grid(row=0, column=0, pady=10, padx=3)
        Gbillbtn = Button(BtnFrame, command=self.g_bill, text="Generate Bill", font=("arial", 12, "bold"), bg="purple",fg="white", pady=10, width=10, bd=7, activebackground="black", activeforeground="white").grid(row=0, column=1, pady=10, padx=3)
        Clearbillbtn = Button(BtnFrame, command=self.clear_bill, text="Clear", font=("arial", 12, "bold"), bg="purple",fg="white", pady=10, width=10, bd=7, activebackground="black",activeforeground="white").grid(row=0, column=2, pady=10, padx=3)
        printbtn = Button(BtnFrame, command=self.print_bill, text="Print", font=("arial", 12, "bold"), bg="purple",fg="white", pady=10, width=10, bd=7, activebackground="black", activeforeground="white").grid(row=0, column=3, pady=10, padx=3)
        exittbtn = Button(BtnFrame, command=self.winexit, text="Exit", font=("arial", 12, "bold"), bg="purple",fg="white", pady=10, width=10, bd=7, activebackground="black", activeforeground="white").grid(row=0, column=4, pady=10, padx=3)

    def total_sum(self):
        global ccashreturn,stockqty1,price1,price2,price3,price4,price5,price6,price7,price8,price9,price10,totalp1,totalp2,totalp3,totalp4,totalp5,totalp6,totalp7,totalp8,totalp9,totalp10
        if self.CnameVar.get() == "" and self.CphoneVar.get() == "":
            messagebox.showerror("Error", "Some fields are required")
        #elif stock1<self.Qty1Var.get():
            #messagebox.showerror("Error", "OOOPS! Product haven't enough stock")
        else:
            self.Qtyone = self.Qty1Var.get()
            self.Qtytwo = self.Qty2Var.get()
            self.Qtythree = self.Qty3Var.get()
            self.Qtyfour = self.Qty4Var.get()
            self.Qtyfive = self.Qty5Var.get()
            self.Qtysix = self.Qty6Var.get()
            self.Qtyseven = self.Qty7Var.get()
            self.Qtyeight = self.Qty8Var.get()
            self.Qtynine = self.Qty9Var.get()
            self.Qtyten = self.Qty10Var.get()


            if self.Qty1Var.get() !=0:
                #========== query For Product One ================
                con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                cur = con.cursor()
                q = "select * from product where title=%s"
                cur.execute(q, (self.ProductOne.get()))
                rows = cur.fetchall()
                for row in rows:
                    self.price1 = row[2]
                    self.totalp1 = self.price1 * self.Qtyone
                con.commit()
                con.close()
            else:
                self.price1 = 0
            self.netprice = float(self.price1*self.Qtyone)

            if self.Qty2Var.get() !=0:
                #========== query For Product Two ================
                con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                cur = con.cursor()
                q = "select * from product where title=%s"
                cur.execute(q, (self.ProductTwo.get()))
                rows = cur.fetchall()
                for row in rows:
                    self.price2 = row[2]
                    self.totalp2 = self.price2 * self.Qtytwo
                con.commit()
                con.close()
            else:
                self.price2 = 0
            self.netprice = float(self.netprice+(self.price2*self.Qtytwo))

            if self.Qty3Var.get() !=0:
                #========== query For Product Three ================
                con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                cur = con.cursor()
                q = "select * from product where title=%s"
                cur.execute(q, (self.ProductThree.get()))
                rows = cur.fetchall()
                for row in rows:
                    self.price3 = row[2]
                    self.totalp3 = self.price3 * self.Qtythree
                con.commit()
                con.close()
            else:
                self.price3 = 0
            self.netprice = float(self.netprice+(self.price3*self.Qtythree))

            if self.Qty4Var.get() !=0:
                #========== query For Product Four ================
                con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                cur = con.cursor()
                q = "select * from product where title=%s"
                cur.execute(q, (self.ProductFour.get()))
                rows = cur.fetchall()
                for row in rows:
                    self.price4 = row[2]
                    self.totalp4 = self.price4 * self.Qtyfour
                con.commit()
                con.close()
            else:
                self.price4 = 0
            self.netprice = float(self.netprice + (self.price4 * self.Qtyfour))

            if self.Qty5Var.get() !=0:
                #========== query For Product Five ================
                con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                cur = con.cursor()
                q = "select * from product where title=%s"
                cur.execute(q, (self.ProductFive.get()))
                rows = cur.fetchall()
                for row in rows:
                    self.price5 = row[2]
                    self.totalp5 = self.price5 * self.Qtyfive
                con.commit()
                con.close()
            else:
                self.price5 = 0
            self.netprice = float(self.netprice + (self.price5 * self.Qtyfive))

            if self.Qty6Var.get() !=0:
                #========== query For Product Six ================
                con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                cur = con.cursor()
                q = "select * from product where title=%s"
                cur.execute(q, (self.ProductSix.get()))
                rows = cur.fetchall()
                for row in rows:
                    self.price6 = row[2]
                    self.totalp6 = self.price6 * self.Qtysix
                con.commit()
                con.close()
            else:
                self.price6 = 0
            self.netprice = float(self.netprice + (self.price6 * self.Qtysix))

            if self.Qty7Var.get() !=0:
                #========== query For Product Seven ================
                con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                cur = con.cursor()
                q = "select * from product where title=%s"
                cur.execute(q, (self.ProductSeven.get()))
                rows = cur.fetchall()
                for row in rows:
                    self.price7 = row[2]
                    self.totalp7 = self.price7 * self.Qtyseven
                con.commit()
                con.close()
            else:
                self.price7 = 0
            self.netprice = float(self.netprice + (self.price7 * self.Qtyseven))

            if self.Qty8Var.get() !=0:
                #========== query For Product Eight ================
                con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                cur = con.cursor()
                q = "select * from product where title=%s"
                cur.execute(q, (self.ProductEight.get()))
                rows = cur.fetchall()
                for row in rows:
                    self.price8 = row[2]
                    self.totalp8 = self.price8 * self.Qtyeight
                con.commit()
                con.close()
            else:
                self.price8 = 0
            self.netprice = float(self.netprice + (self.price8 * self.Qtyeight))

            if self.Qty9Var.get() !=0:
                #========== query For Product Nine ================
                con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                cur = con.cursor()
                q = "select * from product where title=%s"
                cur.execute(q, (self.ProductNine.get()))
                rows = cur.fetchall()
                for row in rows:
                    self.price9 = row[2]
                    self.totalp9 = self.price9 * self.Qtynine
                con.commit()
                con.close()
            else:
                self.price9 = 0
            self.netprice = float(self.netprice + (self.price9 * self.Qtynine))

            if self.Qty10Var.get() !=0:
                #========== query For Product Ten ================
                con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                cur = con.cursor()
                q = "select * from product where title=%s"
                cur.execute(q, (self.ProductTen.get()))
                rows = cur.fetchall()
                for row in rows:
                    self.price10 = row[2]
                    self.totalp10 = self.price10 * self.Qtyten
                con.commit()
                con.close()
            else:
                self.price10 = 0
            self.netprice = float(self.netprice + (self.price10 * self.Qtyten))
            self.totalVar.set(str(self.netprice))

            self.netbill = self.netprice - self.DisVar.get()
            self.netTotalVar.set(str(self.netbill))

            self.cpaycash = self.CpayVar.get()
            if self.cpaycash !=0:
                self.ccashreturn = self.cpaycash - self.netbill
                self.CreturenVar.set(str(self.ccashreturn))

    def welcomebill(self):

        global edate, etime
        self.edate = time.strftime("%d/%m/%Y")
        self.etime = time.strftime("%H:%M:%S")
        # qrimg = PhotoImage(file="qrcodes/6878.png")

        self.txtarea.delete("1.0", END)
        self.txtarea.insert(END, f"\t\t\t Welcome to Our Store \n")
        self.txtarea.insert(END, "\t \t \t Phone No: 017000000000 \n\n")
        self.txtarea.insert(END, "================================================================\n")
        self.txtarea.insert(END, f" Bill No: {self.billnoVar.get()} \n")
        self.txtarea.insert(END, f" Customer Name: {self.CnameVar.get()} \n")
        self.txtarea.insert(END, f" Phone Number: {self.CphoneVar.get()} \n")
        self.txtarea.insert(END, f" Date: {self.edate}, Time: {self.etime} \n")
        self.txtarea.insert(END, "================================================================\n")
        self.txtarea.insert(END, "| Product Name |\t    | Quantity |\t    | Price |\n")
        self.txtarea.insert(END, "================================================================\n\n")


    def g_bill(self):

        mess = messagebox.askyesno("Notification", "Do you want to Generate Bill?", parent=self.billroot)
        if mess > 0:
            global newstock1, newstock2, newstock3, newstock4, newstock5, newstock6, newstock7, newstock8, newstock9, newstock10, oldstock1
            self.blank_sp = "                      "
            self.p1 = self.ProductOne.get() + self.blank_sp
            self.p2 = self.ProductTwo.get() + self.blank_sp
            self.p3 = self.ProductThree.get() + self.blank_sp
            self.p4 = self.ProductFour.get() + self.blank_sp
            self.p5 = self.ProductFive.get() + self.blank_sp
            self.p6 = self.ProductSix.get() + self.blank_sp
            self.p7 = self.ProductSeven.get() + self.blank_sp
            self.p8 = self.ProductEight.get() + self.blank_sp
            self.p9 = self.ProductNine.get() + self.blank_sp
            self.p10 = self.ProductTen.get() + self.blank_sp

            if self.CnameVar.get() == "" or self.CphoneVar.get() == "":
                messagebox.showerror("Error", "Name and Phone number are required!")
            elif self.totalVar.get() == "":
                messagebox.showerror("Error", "No product selected.")
            elif self.ProductOne.get() == "--Select One--" and self.ProductTwo.get() == "--Select One--" and self.ProductThree.get() == "--Select One--" and self.ProductFour.get() == "--Select One--" \
                    and self.ProductFive.get() == "--Select One--" and self.ProductSix.get() == "--Select One--" and self.ProductSeven.get() == "--Select One--" and self.ProductEight.get() == "--Select One--" \
                    and self.ProductNine.get() == "--Select One--" and self.ProductTen.get() == "--Select One--":
                messagebox.showerror("Error", "Please a select product name")
            else:
                self.welcomebill()
                if self.Qty1Var.get() !=0 or self.ProductOne.get() != "--Select One--":
                    self.txtarea.insert(END, f" {self.p1[:17]} \t\t {str(self.Qty1Var.get())}\t\t\t{str(self.totalp1)} \n")
                    #======== Quantity updating on database =============
                    con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                    cur = con.cursor()
                    q = "select * from product where title=%s"
                    cur.execute(q, (self.ProductOne.get()))
                    rows = cur.fetchall()
                    for row in rows:
                        oldstock1 = row[3]
                        newstock1 = oldstock1 - self.Qty1Var.get()
                    q = "update product set qty=%s where title=%s"
                    cur.execute(q,(newstock1,self.ProductOne.get()))
                    con.commit()
                    con.close()

                if self.Qty2Var.get() !=0 or self.ProductTwo.get() != "--Select One--":
                    self.txtarea.insert(END, f" {self.p2[:17]} \t\t {str(self.Qty2Var.get())}\t\t\t{str(self.totalp2)} \n")
                    #======== Quantity updating on database =============
                    con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                    cur = con.cursor()
                    q = "select * from product where title=%s"
                    cur.execute(q, (self.ProductTwo.get()))
                    rows = cur.fetchall()
                    for row in rows:
                        oldstock2 = row[3]
                        newstock2 = oldstock2 - self.Qty2Var.get()
                    q = "update product set qty=%s where title=%s"
                    cur.execute(q,(newstock2,self.ProductTwo.get()))
                    con.commit()
                    con.close()

                if self.Qty3Var.get() !=0 or self.ProductThree.get() != "--Select One--":
                    self.txtarea.insert(END, f" {self.p3[:17]} \t\t {str(self.Qty3Var.get())}\t\t\t{str(self.totalp3)} \n")
                    #======== Quantity updating on database =============
                    con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                    cur = con.cursor()
                    q = "select * from product where title=%s"
                    cur.execute(q, (self.ProductThree.get()))
                    rows = cur.fetchall()
                    for row in rows:
                        oldstock3 = row[3]
                        newstock3 = oldstock3 - self.Qty3Var.get()
                    q = "update product set qty=%s where title=%s"
                    cur.execute(q,(newstock3,self.ProductThree.get()))
                    con.commit()
                    con.close()

                if self.Qty4Var.get() !=0 or self.ProductFour.get() != "--Select One--":
                    self.txtarea.insert(END, f" {self.p4[:17]} \t\t {str(self.Qty4Var.get())}\t\t\t{str(self.totalp4)} \n")
                    #======== Quantity updating on database =============
                    con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                    cur = con.cursor()
                    q = "select * from product where title=%s"
                    cur.execute(q, (self.ProductFour.get()))
                    rows = cur.fetchall()
                    for row in rows:
                        oldstock4 = row[3]
                        newstock4 = oldstock4 - self.Qty4Var.get()
                    q = "update product set qty=%s where title=%s"
                    cur.execute(q,(newstock4,self.ProductFour.get()))
                    con.commit()
                    con.close()

                if self.Qty5Var.get() !=0 or self.ProductFive.get() != "--Select One--":
                    self.txtarea.insert(END, f" {self.p5[:17]} \t\t {str(self.Qty5Var.get())}\t\t\t{str(self.totalp5)} \n")
                    #======== Quantity updating on database =============
                    con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                    cur = con.cursor()
                    q = "select * from product where title=%s"
                    cur.execute(q, (self.ProductFive.get()))
                    rows = cur.fetchall()
                    for row in rows:
                        oldstock5 = row[3]
                        newstock5 = oldstock5 - self.Qty5Var.get()
                    q = "update product set qty=%s where title=%s"
                    cur.execute(q,(newstock5,self.ProductFive.get()))
                    con.commit()
                    con.close()

                if self.Qty6Var.get() !=0 or self.ProductSix.get() != "--Select One--":
                    self.txtarea.insert(END, f" {self.p6[:17]} \t\t {str(self.Qty6Var.get())}\t\t\t{str(self.totalp6)} \n")
                    #======== Quantity updating on database =============
                    con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                    cur = con.cursor()
                    q = "select * from product where title=%s"
                    cur.execute(q, (self.ProductSix.get()))
                    rows = cur.fetchall()
                    for row in rows:
                        oldstock6 = row[3]
                        newstock6 = oldstock6 - self.Qty6Var.get()
                    q = "update product set qty=%s where title=%s"
                    cur.execute(q,(newstock6,self.ProductSix.get()))
                    con.commit()
                    con.close()

                if self.Qty7Var.get() !=0 or self.ProductSeven.get() != "--Select One--":
                    self.txtarea.insert(END, f" {self.p7[:17]} \t\t {str(self.Qty7Var.get())}\t\t\t{str(self.totalp7)} \n")
                    #======== Quantity updating on database =============
                    con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                    cur = con.cursor()
                    q = "select * from product where title=%s"
                    cur.execute(q, (self.ProductSeven.get()))
                    rows = cur.fetchall()
                    for row in rows:
                        oldstock7 = row[3]
                        newstock7 = oldstock7 - self.Qty7Var.get()
                    q = "update product set qty=%s where title=%s"
                    cur.execute(q,(newstock7,self.ProductSeven.get()))
                    con.commit()
                    con.close()

                if self.Qty8Var.get() !=0 or self.ProductEight.get() != "--Select One--":
                    self.txtarea.insert(END, f" {self.p8[:17]} \t\t {str(self.Qty8Var.get())}\t\t\t{str(self.totalp8)} \n")
                    #======== Quantity updating on database =============
                    con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                    cur = con.cursor()
                    q = "select * from product where title=%s"
                    cur.execute(q, (self.ProductEight.get()))
                    rows = cur.fetchall()
                    for row in rows:
                        oldstock8 = row[3]
                        newstock8 = oldstock8 - self.Qty8Var.get()
                    q = "update product set qty=%s where title=%s"
                    cur.execute(q,(newstock8,self.ProductEight.get()))
                    con.commit()
                    con.close()

                if self.Qty9Var.get() !=0 or self.ProductNine.get() != "--Select One--":
                    self.txtarea.insert(END, f" {self.p9[:17]} \t\t {str(self.Qty9Var.get())}\t\t\t{str(self.totalp9)} \n")
                    #======== Quantity updating on database =============
                    con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                    cur = con.cursor()
                    q = "select * from product where title=%s"
                    cur.execute(q, (self.ProductNine.get()))
                    rows = cur.fetchall()
                    for row in rows:
                        oldstock9 = row[3]
                        newstock9 = oldstock9 - self.Qty9Var.get()
                    q = "update product set qty=%s where title=%s"
                    cur.execute(q,(newstock9,self.ProductNine.get()))
                    con.commit()
                    con.close()

                if self.Qty10Var.get() !=0 or self.ProductTen.get() != "--Select One--":
                    self.txtarea.insert(END, f" {self.p10[:17]} \t\t {str(self.Qty10Var.get())}\t\t\t{str(self.totalp10)} \n\n")
                    #======== Quantity updating on database =============
                    con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                    cur = con.cursor()
                    q = "select * from product where title=%s"
                    cur.execute(q, (self.ProductTen.get()))
                    rows = cur.fetchall()
                    for row in rows:
                        oldstock10 = row[3]
                        newstock10 = oldstock10 - self.Qty10Var.get()
                    q = "update product set qty=%s where title=%s"
                    cur.execute(q,(newstock10,self.ProductTen.get()))
                    con.commit()
                    con.close()

                if self.totalVar.get() != 0:
                    self.txtarea.insert(END, "================================================================\n")
                    self.txtarea.insert(END, f"\t\t\t\t\t Total:     {self.totalVar.get()} \n")
                if self.DisVar.get() != 0:
                    self.txtarea.insert(END, f"\t\t\t\t\t Discount : {self.DisVar.get()}\n")
                    self.txtarea.insert(END, "================================================================\n")

                if self.netTotalVar.get() != 0:
                    self.txtarea.insert(END, "================================================================\n")
                    self.txtarea.insert(END, f"\t\t\t\t\t Net Total: {self.netTotalVar.get()}\n")
                    self.txtarea.insert(END, "================================================================\n\n")
                    self.txtarea.insert(END,"Thank you for visiting us.")

                    self.save_bill()

            # ============ Sales Data Inserting to SQL Database =========================
            try:
                if self.CnameVar.get() != "" or self.CphoneVar.get() != "":
                    global bl, na, phn, nbl, dis, dt
                    bl = self.billnoVar.get()
                    na = self.CnameVar.get()
                    phn = self.CphoneVar.get()
                    nbl = self.netTotalVar.get()
                    dis = self.DisVar.get()
                    dt = time.strftime("%d/%m/%Y")
                    con = pymysql.connect(host="localhost", user="root", password="root1234",database="billdata")
                    cur = con.cursor()
                    q = "insert into report values(%s,%s,%s,%s,%s,%s)"
                    cur.execute(q, (bl, na, phn, nbl, dis, dt))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Notification","Data of bill no " + self.billnoVar.get() + " inserted successfully",parent=self.billroot)
                else:
                    messagebox.showerror("Error", "Name and Phone number are required", parent=self.billroot)
            except:
                messagebox.showerror("Error", "Something went wrong with your database", parent=self.billroot)

    def save_bill(self):

        self.data = self.txtarea.get("1.0", END)
        file = open("saveBill/" + str(self.billnoVar.get()) + ".txt", "w")
        file.write(self.data)
        file.close()
        messagebox.showinfo("Saved", "Bill " + self.billnoVar.get() + " saved successfully.", parent=self.billroot)

    def search_bill(self):
        m = "no"
        for i in os.listdir("saveBill/"):
            if i.split(".")[0] == self.billsearchVar.get():
                file = open(f"saveBill/{i}", "r")
                self.txtarea.delete("1.0", END)
                for d in file:
                    self.txtarea.insert(END, d)
                file.close()
                m = "yes"
        if m == "no":
            messagebox.showerror("Error", "Invalid Bill Number.", parent=self.billroot)

    def clear_bill(self):

        mess = messagebox.askyesno("Clear", "Do you want to clear?", parent=self.billroot)
        if mess > 0:
            # ========= Variables ===================

            # ============ customer Info Var ============

            self.CnameVar.set("")
            self.CphoneVar.set("")
            self.billnoVar.set("")

            r_bill = random.randint(1000, 9999)
            self.billnoVar.set(r_bill)

            self.billsearchVar.set("")

            # ============ Products Form Var ============
            self.Qty1Var.set(0)
            self.Qty2Var.set(0)
            self.Qty3Var.set(0)
            self.Qty4Var.set(0)
            self.Qty5Var.set(0)
            self.Qty6Var.set(0)
            self.Qty7Var.set(0)
            self.Qty8Var.set(0)
            self.Qty9Var.set(0)
            self.Qty10Var.set(0)

            self.ProductOne.set("--Select One--")
            self.ProductTwo.set("--Select One--")
            self.ProductThree.set("--Select One--")
            self.ProductFour.set("--Select One--")
            self.ProductFive.set("--Select One--")
            self.ProductSix.set("--Select One--")
            self.ProductSeven.set("--Select One--")
            self.ProductEight.set("--Select One--")
            self.ProductNine.set("--Select One--")
            self.ProductTen.set("--Select One--")

            # ============ Bottom Form Var ============
            self.totalVar.set("")
            self.DisVar.set(0)
            self.netTotalVar.set("")
            self.CpayVar.set(0)
            self.CreturenVar.set("")

            self.txtarea.delete("1.0", END)
            self.welcomebill()

    def print_bill(self):
        mess = messagebox.askyesno("Print", "Do you want print " + self.billnoVar.get() + " ?", parent=self.billroot)
        if mess > 0:
            d = self.txtarea.get("1.0", END)
            temfile = tempfile.mktemp(".txt")
            open(temfile, "w").write(d)
            os.startfile(temfile, "print")

    def winexit(self):
        mess = messagebox.askyesno("Notification", "Do you want to close?", parent=self.billroot)
        if mess > 0:
            self.billroot.quit()


    # =============== Add User window ===========================

    def AddUser(self):
        global userroot,userTable
        userroot = Toplevel()
        userroot.grab_set()
        userroot.geometry("750x500+300+50")
        userroot.title("Billing system - Add User")

        #========== Variable ==============
        self.UserVar = StringVar()
        self.PassVar = StringVar()
        self.RuleVar = StringVar()

        title = Label(userroot, text="Control User", bg="purple", fg="white", font=("arail", 13, "bold"), pady=10)
        title.place(x=0, y=0, relwidth=1)
        adduserFrame = LabelFrame(userroot, text="Add New user", font=("arail", 12, "bold"), fg="gold", bd=7,relief=GROOVE, bg="purple")
        adduserFrame.place(x=0, y=42, width=400, height=450)

        usernamelbl = Label(adduserFrame,text="User Name: ",font=("arial",12,"bold"),bg="purple",fg="white").grid(row=0,column=0,pady=10,padx=10,sticky="w")
        usernametxt = Entry(adduserFrame,textvariable=self.UserVar,width=15,bd=5,relief=SUNKEN,font=("arial",12,"bold")).grid(row=0,column=1,pady=10,padx=10)

        userpasslbl = Label(adduserFrame,text="Password: ",font=("arial",12,"bold"),bg="purple",fg="white").grid(row=1,column=0,pady=10,padx=10,sticky="w")
        userpasstxt = Entry(adduserFrame,textvariable=self.PassVar,width=15,bd=5,relief=SUNKEN,font=("arial",12,"bold")).grid(row=1,column=1,pady=10,padx=10)

        userrulelbl = Label(adduserFrame,text="User Rule: ",font=("arial",12,"bold"),bg="purple",fg="white").grid(row=2,column=0,pady=10,padx=10,sticky="w")
        userruletxt = ttk.Combobox(adduserFrame,textvariable=self.RuleVar,font=("arail",12,"bold"),width=15)
        userruletxt["values"] = ("Admin","User")
        userruletxt.current(1)
        userruletxt.grid(row=2,column=1,pady=10,padx=10)

        useraddbtn = Button(adduserFrame,command=self.user_insert,text="Add User",font=("arail",12,"bold"),bg="black",fg="white",width=15,pady=10).grid(row=4,column=0,pady=10,padx=5)
        userupdatebtn = Button(adduserFrame,command=self.user_update,text="Update",font=("arail",12,"bold"),bg="black",fg="white",width=15,pady=10).grid(row=4,column=1,pady=10,padx=5)
        userdeletebtn = Button(adduserFrame,command=self.user_delete,text="Delete",font=("arail",12,"bold"),bg="black",fg="white",width=15,pady=10).grid(row=5,column=0,pady=10,padx=5)
        exitbtn = Button(adduserFrame,command=self.user_exit,text="Exit",font=("arail",12,"bold"),bg="black",fg="white",width=15,pady=10).grid(row=5,column=1,pady=10,padx=5)

        ShowuserFrame = Frame(userroot,bd=7,relief=GROOVE)
        ShowuserFrame.place(x=400,y=42,height=450,width=350)
        title = Label(ShowuserFrame,text="All Users",font=("arial",12,"bold"),bg="purple",fg="white")
        title.place(x=0,y=0,relwidth=1)

        x_scroll = Scrollbar(ShowuserFrame,orient=HORIZONTAL)
        y_scroll = Scrollbar(ShowuserFrame,orient=VERTICAL)
        userTable = ttk.Treeview(ShowuserFrame,columns=("username","password","rule"),xscrollcommand=x_scroll.set,yscrollcommand=y_scroll.set)
        x_scroll.pack(side=BOTTOM,fill=X)
        y_scroll.pack(side=RIGHT,fill=Y)
        x_scroll.config(command=userTable.xview)
        y_scroll.config(command=userTable.yview)
        userTable.heading("username",text="User Name")
        userTable.heading("password",text="Password")
        userTable.heading("rule",text="User Rule")
        userTable["show"]="headings"
        userTable.column("username",width=50)
        userTable.column("password",width=50)
        userTable.column("rule",width=50)
        userTable.pack(fill=BOTH,expand=1)
        userTable.bind("<ButtonRelease>",self.getuser_cur)
        self.fetch_user()

    def user_insert(self):

        if self.UserVar.get() == "" and self.PassVar.get() == "" and self.RuleVar.get() == "":
            messagebox.showerror("Error", "All Fields are required.", parent=userroot)
        else:
            try:
                self.user = self.UserVar.get()
                self.password = self.PassVar.get()
                self.rule = self.RuleVar.get()

                con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                cur = con.cursor()
                q = "insert into admin values(%s,%s,%s)"
                cur.execute(q, (self.user, self.password, self.rule))
                con.commit()
                self.fetch_user()
                con.close()
                messagebox.showinfo("Notification", "User Added Successfully.", parent=userroot)
                self.UserVar.set("")
                self.PassVar.set("")


            except:
                messagebox.showerror("Error", "User name already exist", parent=userroot)

    def fetch_user(self):
        con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
        cur = con.cursor()
        q = "select * from admin"
        cur.execute(q)
        rows=cur.fetchall()
        userTable.delete(*userTable.get_children())
        for row in rows:
            singleuser=[row[0],row[1],row[2]]
            userTable.insert("",END,values=singleuser)
    def getuser_cur(self, ev):
        cc = userTable.focus()
        content = userTable.item(cc)
        pp = content["values"]
        if len(pp) !=0:
            self.UserVar.set(pp[0])
            self.PassVar.set(pp[1])
            self.RuleVar.set(pp[2])

    def user_update(self):
        mess = messagebox.askyesno("Update","Do you want to update user?",parent=userroot)
        if mess>0:
            con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
            cur = con.cursor()
            q = "update admin set password=%s,rule=%s where username=%s"
            cur.execute(q,(self.PassVar.get(),self.RuleVar.get(),self.UserVar.get()))
            messagebox.showinfo("Notification","User updated Successfully",parent=userroot)
            con.commit()
            self.fetch_user()
            self.UserVar.set("")
            self.PassVar.set("")
            con.close()
    def user_delete(self, ev):
        mess = messagebox.askyesno("Update","Do you want to delete user?",parent=userroot)
        if mess>0:
            con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
            cur = con.cursor()
            q = "delete from admin where username=%s"
            self.UserVar.get()
            cur.execute(q,(self.UserVar.get()))
            messagebox.showinfo("Notification","User deleted Successfully",parent=userroot)
            con.commit()
            self.fetch_user()
            self.UserVar.set("")
            self.PassVar.set("")
            con.close()
    def user_exit(self):
        mess = messagebox.askyesno("Exit","Do you want to close?",parent=userroot)
        if mess>0:
            userroot.destroy()
#=============== Add Products window ===========================
    def AddPro(self):
        global proot,produttable
        proot = Toplevel()
        proot.grab_set()
        proot.geometry("750x600+300+50")
        proot.title("Billing system")

        title =Label(proot,text="Add New Products",bg="purple",fg="white",font=("arail",13,"bold"),pady=10)
        title.place(x=0,y=0,relwidth=1)


        #============ Variables =========

        self.idVar = StringVar()
        self.titleVar = StringVar()
        self.priceVar = StringVar()
        self.qtyVar = StringVar()

        pFrame = LabelFrame(proot,text="Add Product Details",font=("arail",12,"bold"),fg="gold",bd=7,relief=GROOVE,bg="purple")
        pFrame.place(x=0,y=42,width=400,height=450)

        product_idlbl =Label(pFrame,text="Product Code",font=("arial", 12,"bold"),bg="purple",fg="white").grid(row=0,column=0,pady=5,padx=10,sticky="w")
        Product_idtxt = Entry(pFrame,textvariable=self.idVar,width=15,bd=5,relief=SUNKEN,font=("arial",12,"bold")).grid(row=0,column=1,pady=5,padx=10)

        product_namelbl =Label(pFrame,text="Product Title",font=("arial", 12,"bold"),bg="purple",fg="white").grid(row=1,column=0,pady=5,padx=10,sticky="w")
        Product_nametxt = Entry(pFrame,textvariable=self.titleVar,width=15,bd=5,relief=SUNKEN,font=("arial",12,"bold")).grid(row=1,column=1,pady=5,padx=10)

        product_pricelbl =Label(pFrame,text="Product Price",font=("arial", 12,"bold"),bg="purple",fg="white").grid(row=2,column=0,pady=5,padx=10,sticky="w")
        Product_pricetxt = Entry(pFrame,textvariable=self.priceVar,width=15,bd=5,relief=SUNKEN,font=("arial",12,"bold")).grid(row=2,column=1,pady=5,padx=10)

        product_qtylbl =Label(pFrame,text="Product Quantity",font=("arial", 12,"bold"),bg="purple",fg="white").grid(row=3,column=0,pady=5,padx=10,sticky="w")
        Product_qtytxt = Entry(pFrame,textvariable=self.qtyVar,width=15,bd=5,relief=SUNKEN,font=("arial",12,"bold")).grid(row=3,column=1,pady=5,padx=10)

        #=========== Data Table Frame ====================
        dataFrame = Frame(proot,bd=7,relief=GROOVE)
        dataFrame.place(y=42,x=400,width=350,height=450)

        title = Label(dataFrame,text="Products",font=("arial", 12,"bold"),bg="black",fg="white",pady=5)
        title.place(x=0,y=0, relwidth=1)
        scroll_x = Scrollbar(dataFrame,orient=HORIZONTAL)
        scroll_y = Scrollbar(dataFrame,orient=VERTICAL)
        produttable = ttk.Treeview(dataFrame,columns=("id","title","price","qty"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=produttable.xview)
        scroll_y.config(command=produttable.yview)
        produttable.heading("id",text="ID")
        produttable.heading("title",text="Title")
        produttable.heading("price",text="Price")
        produttable.heading("qty",text="Quantity")
        produttable["show"]="headings"
        produttable.column("id",width=50)
        produttable.column("title",width=150)
        produttable.column("price",width=50)
        produttable.column("qty",width=50)
        produttable.pack(fill=BOTH,expand=1)
        produttable.bind("<ButtonRelease>",self.get_curcur)
        self.fetch_data()



        #=========== Buttons Frame =======================
        btnFrame = LabelFrame(proot, text="Buttons", font=("arail", 12, "bold"), fg="gold", bd=7,relief=GROOVE, bg="purple")
        btnFrame.place(x=0, y=490, relwidth=1, height=120)

        addbtn = Button(btnFrame,command=self.addproduct,text="Submit Data",font=("arial",12,"bold"),bd=5,pady=5,width=10).grid(row=0,column=0,pady=15,padx=10)
        updatebtn = Button(btnFrame,command=self.pupdate,text="Update",font=("arial",12,"bold"),bd=5,pady=5,width=10).grid(row=0,column=1,pady=15,padx=10)
        clearbtn = Button(btnFrame,command=self.pclear,text="Clear",font=("arial",12,"bold"),bd=5,pady=5,width=10).grid(row=0,column=2,pady=15,padx=10)
        deletebtn = Button(btnFrame,command=self.pdelete,text="Delete",font=("arial",12,"bold"),bd=5,pady=5,width=10).grid(row=0,column=3,pady=15,padx=10)
        exitbtn = Button(btnFrame,command=self.pexit,text="Exit",font=("arial",12,"bold"),bd=5,pady=5,width=10).grid(row=0,column=4,pady=15,padx=10)

    #========== Insert products into database ===========================
    def addproduct(self):
        global pid
        if self.idVar.get()=="" and self.titleVar.get()=="" and self.priceVar.get()=="" and self.qtyVar.get()=="":
            messagebox.showerror("Error","All fields are required.",parent=proot)
        else:
            self.pid = self.idVar.get()
            self.title = self.titleVar.get()
            self.price = self.priceVar.get()
            self.qty = self.qtyVar.get()
            try:
                con = pymysql.connect(host="localhost",user="root",password="root1234",database="billdata")
                cur= con.cursor()
                q = "insert into product values(%s,%s,%s,%s)"
                cur.execute(q,(self.pid, self.title, self.price, self.qty))
                con.commit()
                con.close()
                messagebox.showinfo("Notification","Product added successfully",parent=proot)

                self.idVar.set("")
                self.titleVar.set("")
                self.priceVar.set("")
                self.qtyVar.set("")
                self.fetch_data()
            except:
                messagebox.showerror("Error","Something went wrong with database",parent=proot)
    def fetch_data(self):
        try:
            con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
            cur = con.cursor()
            q = "select * from product"
            cur.execute(q)
            rows = cur.fetchall()
            produttable.delete(*produttable.get_children())
            for row in rows:
                single = [row[0], row[1], row[2], row[3]]
                produttable.insert("", END, values=single)
        except:
            messagebox.showerror("Error", "Something went wrong with database", parent=proot)
    def get_curcur(self,ev):
        cc = produttable.focus()
        content = produttable.item(cc)
        p = content["values"]
        if p!=0:
            self.idVar.set(p[0])
            self.titleVar.set(p[1])
            self.priceVar.set(p[2])
            self.qtyVar.set(p[3])
    def pupdate(self):
        mess = messagebox.askyesno("Notification","Do you want to update data?", parent=proot)
        if mess>0:
            try:
                con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                cur = con.cursor()
                q = "update product set title=%s,price=%s,qty=%s where id=%s"
                cur.execute(q,(self.titleVar.get(),self.priceVar.get(),self.qtyVar.get(),self.idVar.get()))
                con.commit()
                self.fetch_data()
                self.idVar.set("")
                self.titleVar.set("")
                self.priceVar.set("")
                self.qtyVar.set("")
                con.close()
            except:
                messagebox.showerror("Error", "Something went wrong with database", parent=proot)
    def pdelete(self):
        mess = messagebox.askyesno("Notification","Do you want to Delete?", parent=proot)
        if mess>0:
            try:
                con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
                cur = con.cursor()
                q = "delete from product where id=%s"
                cur.execute(q,(self.idVar.get()))
                con.commit()
                self.fetch_data()
                self.idVar.set("")
                self.titleVar.set("")
                self.priceVar.set("")
                self.qtyVar.set("")
                con.close()
            except:
                messagebox.showerror("Error", "Something went wrong with database", parent=proot)
    def pclear(self):
        mess = messagebox.askyesno("Exit","Do you want to Clear?", parent=proot)
        if mess >0:
            self.idVar.set("")
            self.titleVar.set("")
            self.priceVar.set("")
            self.qtyVar.set("")
    def pexit(self):
        mess = messagebox.askyesno("Exit","Do you want to Exit?", parent=proot)
        if mess >0:
            #self.billroot.destroy()
            proot.destroy()
            #self.billingapp()

#=============== Report window ===========================
    def rewin(self):
        global reroot,reFrame
        reroot = Toplevel()
        reroot.grab_set()
        reroot.title("Sales Report")
        reroot.geometry("1000x650+200+30")
        title = Label(reroot,text="Daily Sales Report",font=("arial",15,"bold"),bg="purple",fg="white")
        title.pack(fill=X,side=TOP)

        #=====================Variable ===================
        global nameVar, phonVar,billVar,dateVar,reportTable
        self.nameVar = StringVar()
        self.phnVar = StringVar()
        self.billVar = StringVar()
        self.dateVar = StringVar()

        sFrame = LabelFrame(reroot,text="Search Area",font=("arial",12,"bold"),fg="gold",bg="purple",bd=7,relief=GROOVE)
        sFrame.place(x=0,y=30,relwidth=1,height=100)

        namelbl = Label(sFrame,text="Name: ",font=("arial",12,"bold"),fg="white",bg="purple").grid(row=0,column=0,padx=5,pady=10,sticky="w")
        nameEntry = Entry(sFrame,textvariable=self.nameVar,width=13,bd=5,relief=SUNKEN,font=("arial",12,"bold")).grid(row=0,column=1,pady=10,padx=5)

        phonelbl = Label(sFrame,text="Phone: ",font=("arial",12,"bold"),fg="white",bg="purple").grid(row=0,column=2,padx=5,pady=10,sticky="w")
        phoneEntry = Entry(sFrame,textvariable=self.phnVar,width=13,bd=5,relief=SUNKEN,font=("arial",12,"bold")).grid(row=0,column=3,pady=10,padx=5)

        billnolbl = Label(sFrame,text="Bill No: ",font=("arial",12,"bold"),fg="white",bg="purple").grid(row=0,column=4,padx=5,pady=10,sticky="w")
        billnoEntry = Entry(sFrame,textvariable=self.billVar,width=13,bd=5,relief=SUNKEN,font=("arial",12,"bold")).grid(row=0,column=5,pady=10,padx=5)

        datelbl = Label(sFrame,text="Date: ",font=("arial",12,"bold"),fg="white",bg="purple").grid(row=0,column=6,padx=5,pady=10,sticky="w")
        dateEntry = Entry(sFrame,textvariable=self.dateVar,width=13,bd=5,relief=SUNKEN,font=("arial",12,"bold")).grid(row=0,column=7,pady=10,padx=5)

        searchbtn = Button(sFrame,command=self.filter,text="Filter",font=("arial",11,"bold"),bd=5,width=10).grid(row=0,column=8,pady=10,padx=5)


        reFrame = LabelFrame(reroot,text="Report",font=("arial", 12,"bold"),fg="gold",bd=5,relief=GROOVE,bg="black")
        reFrame.place(x=0,y=130,relwidth=1,height=450)

        ##------------ Show Data Frame -----------------------------------------
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("arial", 10, "bold"))
        style.configure("Treeview", font=("arial", 10, "bold"),bg="skyblue")
        scroll_x = Scrollbar(reFrame,orient=HORIZONTAL)
        scroll_y = Scrollbar(reFrame,orient=VERTICAL)
        reportTable = ttk.Treeview(reFrame,columns=("bill_no","Name","Phone","Net Total", "Discount", "Date"),xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=reportTable.xview)
        scroll_y.config(command=reportTable.yview)
        reportTable.heading("bill_no", text="Bill Number")
        reportTable.heading("Name", text="Customer Name")
        reportTable.heading("Phone", text="Phone Number")
        reportTable.heading("Net Total", text="Net Total")
        reportTable.heading("Discount", text="Discount")
        reportTable.heading("Date", text="Date")
        reportTable["show"]="headings"
        reportTable.column("bill_no",width=100)
        reportTable.column("Name",width=200)
        reportTable.column("Phone",width=100)
        reportTable.column("Net Total",width=100)
        reportTable.column("Discount",width=100)
        reportTable.column("Date",width=150)
        reportTable.pack(fill=BOTH, expand=1)
        reportTable.bind("<ButtonRelease>",self.reget_cur)
        self.show_all()


        try:
            global sum,Total,namesum
            con = pymysql.connect(host="localhost",user="root", password="root1234",database="billdata")
            cur = con.cursor()
            q = "select * from report"
            cur.execute(q)
            con.commit()
            rows = cur.fetchall()
            reportTable.delete(*reportTable.get_children())
            sum = 0
            for row in rows:
                singlerow = [row[0],row[1],row[2],row[3],row[4],row[5]]
                reportTable.insert("",END, values=singlerow)
                sum = sum+row[3]

        except:
            messagebox.showerror("Error","Something went wront with database",parent=reroot)

        BtnFrame = LabelFrame(reroot,text="Buttons",font=("arail",12,"bold"),fg="gold",bg="purple",relief=GROOVE)
        BtnFrame.place(x=0,y=580,relwidth=1,height=70)

        exportbtn = Button(BtnFrame,command=self.export,text="Export",font=("arial",12,"bold"),bd=5,width=10).grid(row=0,column=0,padx=10,pady=5)
        clearbtn = Button(BtnFrame,command=self.clear,text="Clear",font=("arial",12,"bold"),bd=5,width=10).grid(row=0,column=1,padx=10,pady=5)
        showbtn = Button(BtnFrame,command=self.show_all,text="Show All",font=("arial",12,"bold"),bd=5,width=10).grid(row=0,column=2,padx=10,pady=5)
        deletebtn = Button(BtnFrame,command=self.redelete,text="Delete",font=("arial",12,"bold"),bd=5,width=10).grid(row=0,column=3,padx=10,pady=5)
        exitbtn = Button(BtnFrame,command=self.reexit,text="Exit",font=("arial",12,"bold"),bd=5,width=10).grid(row=0,column=4,padx=10,pady=5)

        Totallife = Label(BtnFrame,text="Lifetime: BDT "+str(sum), font=("arial",12,"bold"),bg="purple",fg="white").grid(row=0,column=5,padx=10,pady=5)



    def filter(self):
        global bill,name,phone,date,namesum
        bill = self.billVar.get()
        name = self.nameVar.get()
        phone = self.phnVar.get()
        date = time.strftime("%d/%m/%Y")

        if bill !="":
            con = pymysql.connect(host="localhost",user="root", password="root1234",database="billdata")
            cur = con.cursor()
            q = "select * from report where bill_no=%s"
            cur.execute(q,(self.billVar.get()))
            con.commit()
            rows = cur.fetchall()
            reportTable.delete(*reportTable.get_children())

            for row in rows:
                singlerow = [row[0],row[1],row[2],row[3],row[4],row[5]]
                reportTable.insert("",END, values=singlerow)

        elif name !="":
            con = pymysql.connect(host="localhost",user="root", password="root1234",database="billdata")
            cur = con.cursor()
            q = "select * from report where name=%s"
            cur.execute(q,(name))
            con.commit()
            rows = cur.fetchall()
            reportTable.delete(*reportTable.get_children())
            for row in rows:
                singlerow = [row[0],row[1],row[2],row[3],row[4],row[5]]
                reportTable.insert("",END, values=singlerow)

        elif phone !="":
            con = pymysql.connect(host="localhost",user="root", password="root1234",database="billdata")
            cur = con.cursor()
            q = "select * from report where phone=%s"
            cur.execute(q,(phone))
            con.commit()
            rows = cur.fetchall()
            reportTable.delete(*reportTable.get_children())
            for row in rows:
                singlerow = [row[0],row[1],row[2],row[3],row[4],row[5]]
                reportTable.insert("",END, values=singlerow)

        elif date !="":
            con = pymysql.connect(host="localhost",user="root", password="root1234",database="billdata")
            cur = con.cursor()
            q = "select * from report where date=%s"
            cur.execute(q,(self.dateVar.get()))
            con.commit()
            rows = cur.fetchall()
            reportTable.delete(*reportTable.get_children())
            for row in rows:
                singlerow = [row[0],row[1],row[2],row[3],row[4],row[5]]
                reportTable.insert("",END, values=singlerow)

    def export(self):
        mess = messagebox.askyesno("Export","Do you want to export data?",parent=reroot)
        if mess>0:

            global file,reFrame
            file = filedialog.asksaveasfilename()
            data = reportTable.get_children()

            bill,name,phone,total,discount,date=[],[],[],[],[],[]
            for i in data:
                content = reportTable.item(i)

                pp = content["values"]
                bill.append(pp[0]),
                name.append(pp[1])
                phone.append(pp[2])
                total.append(pp[3])
                discount.append(pp[4])
                date.append(pp[5])
            hh = ["Bill No","Name","Phone","Net Total","Discount","Date"]
            df= pandas.DataFrame(list(zip(bill,name,phone,total,discount,date)),columns=hh)
            paths = r"{}.csv".format(file)
            df.to_csv(paths,index=False)
            messagebox.showinfo("Saved", "File Save Successfully",parent=reroot)

    def clear(self):
        self.nameVar.set("")
        self.phnVar.set("")
        self.billVar.set("")
        self.dateVar.set("")
    def show_all(self):
        con = pymysql.connect(host="localhost", user="root", password="root1234", database="billdata")
        cur = con.cursor()
        q = "select * from report"
        cur.execute(q)
        con.commit()
        rows = cur.fetchall()

        reportTable.delete(*reportTable.get_children())
        for row in rows:
            singlerow = [row[0], row[1], row[2], row[3], row[4], row[5]]
            reportTable.insert("", END, values=singlerow)
        self.clear()
    def redelete(self):
        mess = messagebox.askyesno("Delete","Do you want to delete record?",parent=reroot)
        if mess>0:
            con=pymysql.connect(host="localhost",user="root",password="root1234",database="billdata")
            cur=con.cursor()
            q = "delete from report where bill_no=%s"
            cur.execute(q,(self.billVar.get()))
            con.commit()
            self.clear()
            self.show_all()
            con.close()
            messagebox.showinfo("Deleted","Record deleted successfully.",parent=reroot)
            reroot.destroy()
            self.rewin()
    def reget_cur(self,ev):
        cc = reportTable.focus()
        content = reportTable.item(cc)
        pp = content["values"]
        if len(pp)!=0:
            self.billVar.set(pp[0])
    def reexit(self):
        mess = messagebox.askyesno("Exit","Do you want to exit?", parent=reroot)
        if mess>0:
            reroot.destroy()




root = Tk()
obj = LoginWin(root)
root.mainloop()



