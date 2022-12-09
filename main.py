#Importing Libraries 
from tkinter import *
from tkinter import ttk
import datetime as dt
from mydb import *
from tkinter import messagebox
import customtkinter

# Creating Objecxt for Database
data=Database(db='test.db')
count=0
selected_rowid=0

def saveRecord():
    global data
    data.insertRecord(item_name=item_name.get(),item_price=item_amt.get(),purchase_date=transaction_date.get())

def setDate():
    date=dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')



def clearRecords():
    item_name.delete(0,'end')
    item_amt.delete(0,'end')
    transaction_date.delete(0,'end')

def fetch_records():
    f=data.fetchRecord('select rowid, * from expense_record')
    global count
    for rec in f:
        tv.insert(parent='',index='0',iid=count,values=(rec[0],rec[1],rec[2],rec[3]))
        count+=1
    tv.after(400,refreshData)

def select_record(event):
    global selected_rowid
    selected=tv.focus()
    val=tv.item(selected,'values')

    try:
        selected_rowid=val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
    except Exception as ep:
        pass
    
def update_record():
    global selected_rowid

    selected=tv.focus()

    try:
        data.updateRecord(namevar.get(),amtvar.get(),dopvar.get(),selected_rowid)
        tv.item(selected,text="",values=(namevar.get(),amtvar.get(),dopvar.get()))
    except Exception as ep:
        messagebox.showerror("Error",ep)

    item_name.delete(0, END)
    item_amt.delete(0, END)
    transaction_date.delete(0, END)
    tv.after(400, refreshData)

def totalBalance():
    f=data.fetchRecord(query="Select sum(item_price) from expense_record")
    for i in f:
        for j in i:
            messagebox.showinfo('Current Balance: ',f"Total Expense: '{j} \n Balance Remaining : {10000-j}")


def refreshData():
    for item in tv.get_children():
        tv.delete(item)
    fetch_records()

def deleteRow():
    global selected_rowid
    data.removeRecord(selected_rowid)
    refreshData()

# Creation of GUI
ws=customtkinter.CTk()
ws.title("Daily Expenses")
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")

f=("Verdana", 24)
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()

# Frame Widget
f2 = customtkinter.CTkFrame(ws)
f2.pack()

f1 = customtkinter.CTkFrame(ws)
f1.pack(expand=True,fill=BOTH)

#Labels
customtkinter.CTkLabel(f1,text='ITEM NAME',font=f,corner_radius=8).grid(row=0, column=0, sticky=W)
customtkinter.CTkLabel(f1,text='ITEM PRICE',font=f,corner_radius=8).grid(row=1, column=0, sticky=W)
customtkinter.CTkLabel(f1,text='PURCHASE DATE',font=f,corner_radius=8).grid(row=2, column=0, sticky=W)

# Entry Widgets
item_name = customtkinter.CTkEntry(f1,font=f,width=350,height=25,corner_radius=10,textvariable=namevar)
item_amt = customtkinter.CTkEntry(f1,font=f,width=350,height=25,corner_radius=10,textvariable=amtvar)
transaction_date = customtkinter.CTkEntry(f1,font=f,width=350,height=25,corner_radius=10,textvariable=dopvar)


# Entry grid placement
item_name.grid(row=0,column=1,sticky=EW,padx=(10,0))
item_amt.grid(row=1,column=1,sticky=EW,padx=(10,0))
transaction_date.grid(row=2,column=1,sticky=EW,padx=(10,0))

# Action Buttons
cur_date = customtkinter.CTkButton(
    f1,
    text='Current Date',
    font=f,
    command=setDate,
    corner_radius=10,
    width=15
)

submit_btn=customtkinter.CTkButton(
    f1,
    text='Save Record',
    font=f,
    corner_radius=10,
    command=saveRecord,
    height=10
   
)

clr_btn=customtkinter.CTkButton(
    f1,
    text='Clear Entry',
    font=f,
    corner_radius=10,
    command=clearRecords
   
)

quit_btn=customtkinter.CTkButton(
    f1,
    text='Exit',
    font=f,
    corner_radius=10,
    command=lambda:ws.destroy()
 
)

total_bal=customtkinter.CTkButton(
    f1,
    text='Total balance',
    font=f,
    corner_radius=10,
    command=totalBalance

)
# total_spent=Button(
#     f1,
#     text='Total Spent',
#     font=f,
#     bg='#486966',
#     command=lambda:data.fetchRecord('select sum(ite)')

# )

update_btn = customtkinter.CTkButton(
    f1, 
    text='Update',
    command=update_record,
    corner_radius=10,
    font=f
)

del_btn = customtkinter.CTkButton(
    f1, 
    text='Delete',
    corner_radius=10,
    command=deleteRow,
    font=f
)
#10 Button grid placement
cur_date.grid(row=3, column=1, sticky=EW, padx=(10, 0))
submit_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0))
clr_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
quit_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
total_bal.grid(row=0, column=3, sticky=EW, padx=(10, 0))
update_btn.grid(row=1, column=3, sticky=EW, padx=(10, 0))
del_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0))


#TreeView
tv=ttk.Treeview(f2,columns=(1,2,3,4),show='headings',height=18)
tv.pack(side="left")

#add heading to treeview
tv.column("# 1", anchor=CENTER, stretch=NO, width=295)
tv.column("# 2", anchor=CENTER, stretch=NO, width=295)
tv.column("# 3", anchor=CENTER, stretch=NO, width=295)
tv.column("# 4", anchor=CENTER, stretch=NO, width=295)

tv.heading("# 1",text="Serial No")
tv.heading("# 2",text="Item Name")
tv.heading("# 3",text="Item Price")
tv.heading("# 4",text="Purchase Date")

tv.bind("<ButtonRelease-1>",select_record)

style = ttk.Style()
style.theme_use('alt')
style.configure('Treeview.Heading', background="#4aa153",height=15,foreground='white',font=(None, 20))
style.configure('Treeview',rowheight=30,background="white",fieldbackground="grey",font=(None, 20))
style.map("Treeview",background=[('selected','red')])

#Vertical Scrollbar
scrollbar = customtkinter.CTkScrollbar(f2)
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)

#calling functions
fetch_records()
ws.mainloop()