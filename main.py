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





root = Tk()
obj = LoginWin(root)
root.mainloop()



