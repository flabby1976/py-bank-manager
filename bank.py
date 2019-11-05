# For the GUI 
from tkinter import *
# import tkFileDialog
# import tkMessageBox
from tkinter import filedialog, messagebox

from ofxparse import OfxParser

import csv
import sys
import time

import re

# from pprint import pprint

my_name = "py-bank-manager "
my_version = "Version 0.1 "
my_author = "Andrew Robinson "

full_list = []
cats_dict = {}


def new_file():
    global full_list

    full_list = []
    print("New File!")


def read_cats():
    global cats_dict

    name = filedialog.askopenfilename()
    with open(name, 'r') as foo:
        reader = csv.reader(foo)
        cats_dict = {}
        for k, v in reader:
            cats_dict[k] = v

    print("meeowwww")


def apply_cats():
    global full_list

    for entry in full_list:
        if not entry["Description"] in cats_dict:
            cats_dict[entry["Description"]] = ""

        entry["Category"] = cats_dict[entry["Description"]]

    print('woof!!')


def read_ofx():
    global full_list

    names = filedialog.askopenfilenames()

    for name in names:
        print(name)

        with open(name, 'r') as ofx_file:
            ofx = OfxParser.parse(ofx_file)

            accounts = ofx.accounts

            for a in accounts:
                print(a.account_id, a.institution, a.account_type)

                transactions = a.statement.transactions

                for t in transactions:
                    entry = {"Account": a.number, "Date": t.date, "Amount": t.amount}
                    k = t.memo + " " + t.payee
                    # replace multiple spaces with single
                    k = re.sub(r'\s\s+', " ", k)
                    entry["Description"] = k

                    if not entry["Description"] in cats_dict:
                        cats_dict[entry["Description"]] = ""

                    entry["Category"] = cats_dict[entry["Description"]]

                    full_list.append(entry)

    # sort the list in ascending date order
    full_list = sorted(full_list, key=lambda dum: dum["Date"])


def write_file():

    with open('eggs.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)

        for entry in full_list:
            print(entry)
            spamwriter.writerow([entry["Account"], time.strftime('%d-%b-%Y', entry["Date"].timetuple()),
                                 entry["Amount"], entry["Description"], entry["Category"]])

    csvfile.close()

    with open('cats.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)

        for k, v in cats_dict.items():
            spamwriter.writerow([k, v])

    csvfile.close()

    print("Exported!")


def about():
    messagebox.showinfo("About", my_name + "\n" + my_version + "\n" + my_author)


root = Tk()
root.title('py-bank-manager - bank statement processor')
root.iconbitmap(default='flag.ico')

t1 = Text(root)
sb = Scrollbar(root)
t1.pack(side=LEFT, fill=Y)
sb.pack(side=RIGHT, fill=Y)
sb.config(command=t1.yview)
t1.config(yscrollcommand=sb.set)


# Redirect print to the root widow text box
class PrintToT1(object):
    @staticmethod
    def write(s):
        t1.insert(END, s)
        t1.see(END)


sys.stdout = PrintToT1()
sys.stderr = PrintToT1()

menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=new_file)
filemenu.add_separator()
filemenu.add_command(label="Import OFX...", command=read_ofx)
filemenu.add_separator()
filemenu.add_command(label="Export ...", command=write_file)
filemenu.add_separator()
filemenu.add_command(label="Read Cats ...", command=read_cats)
filemenu.add_command(label="Apply Cats ...", command=apply_cats)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=about)

mainloop()
