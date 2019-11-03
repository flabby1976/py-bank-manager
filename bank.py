# For the GUI 
from Tkinter import *
import tkFileDialog 
import tkMessageBox

from ofxparse import OfxParser

import csv
import sys
import time

import re

from pprint import pprint

Myname = "banktool "
Myversion = "Version 0.1 "
Myauthor = "Andrew Robinson "

full_list = []
cats_dict ={}

def ApplyCats():

    global full_list
    global cats_dict
    
    for entry in full_list:
        if not entry["Description"] in cats_dict:
            cats_dict[entry["Description"]] = ""
            
        entry["Category"]=cats_dict[entry["Description"]]
        

def ReadOFX():

    global full_list
    global cats_dict
    
    names = tkFileDialog.askopenfilenames()

    for name in names:
        print name
        
        ofxfile=open(name, 'r')
        ofx = OfxParser.parse(ofxfile)

        accounts = ofx.accounts

        for a in accounts:
            print a.account_id, a.institution, a.account_type
            
            transactions = a.statement.transactions

            for t in transactions:

##                print t.__dict__
                
                entry={"Account": a.number}
#                entry["Date"]=time.strptime(t.date,'%Y-%m-%d %H:%M:%S')
                entry["Date"]=t.date
                entry["Amount"]=t.amount
                k=t.memo+" "+t.payee
                k = re.sub("\s\s+", " ", k)
                entry["Description"]=k

                if not entry["Description"] in cats_dict:
                    cats_dict[entry["Description"]] = ""
                    
                entry["Category"]=cats_dict[entry["Description"]]

                full_list.append(entry)

        ofxfile.close()

    full_list=sorted(full_list,key=lambda k: k["Date"], reverse=False)


def NewFile():
    full_list = []
    print "New File!"

def ReadCats():
    global cats_dict
    
    name = tkFileDialog.askopenfilename()
    foo = open(name, 'r')
    reader = csv.reader(foo)
    cats_dict = {}
    for k, v in reader:
        cats_dict[k] = v

    foo.close()

    print("meeowwww")


def WriteFile():
    global full_list

    with open('eggs.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile)

        for entry in full_list:
            spamwriter.writerow([entry["Account"], time.strftime('%d-%b-%Y', entry["Date"].timetuple()), entry["Amount"], entry["Description"], entry["Category"] ])

    csvfile.close()

    with open('cats.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile)

        for k, v in cats_dict.items():
            spamwriter.writerow([k , v ])

    csvfile.close()
   
    print "Exported!"
    
            
def About():
    tkMessageBox.showinfo("About", Myname + "\n" + Myversion + "\n" + Myauthor)
    
root = Tk()
root.title('banktool - bank statement processor')
root.iconbitmap(default='flag.ico')

t1=Text(root)
s = Scrollbar(root)
t1.pack(side=LEFT, fill=Y)
s.pack(side=RIGHT, fill=Y)
s.config(command=t1.yview)
t1.config(yscrollcommand=s.set)

#Redirect print to the root widow text box
class PrintToT1(object): 
     def write(self, s): 
         t1.insert(END, s)
         t1.see(END)
sys.stdout = PrintToT1()
sys.stderr = PrintToT1()

menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=NewFile)
filemenu.add_separator()
filemenu.add_command(label="Import OFX...", command=ReadOFX)
filemenu.add_separator()
filemenu.add_command(label="Export ...", command=WriteFile)
filemenu.add_separator()
filemenu.add_command(label="Read Cats ...", command=ReadCats)
filemenu.add_command(label="Apply Cats ...", command=ApplyCats)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

mainloop()
