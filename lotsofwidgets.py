from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import simpledialog as sd
import sqlite3 as sql
import re

def format_ls_str(ls):
    fls = []
    for i in range(0,len(ls)):
        ustr = ls[i]
        fstr = re.sub(r'(?<!^)(?=[A-Z])', ' ', ustr)
        tls = list(fstr)
        tls[0] = tls[0].upper()
        tstr = ""
        for j in range(0,len(tls)):
            tstr += tls[j]
        fstr = tstr
        fls.append(ustr)
        fls.append(fstr)
    return fls

def make_table(n,ls,t,add_funs=False):
    s = """
con = sql.connect('main.db')
c = con.cursor()
        """
    exec(s)
    s = f'''
c.execute("""CREATE TABLE IF NOT EXISTS {n}(
            {n}id integer primary key UNIQUE NOT NULL,
        '''
    for i in range(0,len(ls)):
        if i != len(ls)-1:
            s +=f'''
            \n{ls[i]} {t[i]},
            '''
        else:
            s += f'''
            \n{ls[i]} {t[i]}
            )""")
                        '''
    exec(s)

    if add_funs == True:
        s = f'''
global add_{n}
add_{n}({ls}):
    c.execute("""INSERT INTO {n}
                ({ls}) VALUES
                (
            '''
        for i in range(0,len(ls)):
            if i < len(ls)-1:
                s += ls[i] + ", :"
            else:
                s += ls[i] + ')""",{'
        for i in range(0,len(ls)):
            if i < len(ls)-1:
                s += f'"{ls[i]}:{ls[i]},"'
            else:
                s += '})'
        s += '''
    con.commit()
            '''
        exec(s)
        
def make_entries_with_labels(f,ls,fnt="",size="",pdx=0,pdy=0,bg="white",fg="black"):
    fls = format_ls_str(ls)
    for i in range(0,len(fls),2):
        v = fls[i]
        d = fls[i-1]
        s = f'''
global {v}l
{v}l = Label({f},text="{d}",font="{fnt} {size}",padx={pdx},pady={pdy},bg="{bg}",fg="{fg}")
{v}l.grid(row={i},column=0,sticky=W)
global {v}e
{v}e = Entry({f})
{v}e.grid(row={i},column=1,sticky=W)
        '''
    print(s)
    exec(s)
accls = ["user","role","pass"]
acct = ["string","string","string"]

win = Tk()
win.title("Test Window")
win.geometry("300x300")

mainf = Frame(win)
mainf.pack()

make_entries_with_labels("mainf",accls,"Helvetica","12",None,None,"#00ff00")
make_table("drugs",accls,acct,add_funs=True)

win.mainloop()