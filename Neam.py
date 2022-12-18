import tkinter as tk
import mysql.connector
from tkinter import ttk
from tkinter import *

def projectSubmit():
    prname = project_name.get()
    prnumber = project_number.get()

    addNewProject(prname, prnumber)

def addNewProject(prname, prnumber):
    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 password="1234",
                                 db="Neam")
    cursor = db.cursor()
    sql = "INSERT INTO projects (project_name, project_number) VALUES (%s, %s)"
    val = (prname, prnumber)

    cursor.execute(sql, val)
    db.commit()
    db.close()

def viewProjects():
    for i in tree.get_children():
        tree.delete(i)

    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 password="1234",
                                 db="Neam")
    cursor = db.cursor()
    sql = "SELECT * FROM projects"

    cursor.execute(sql)
    myresult = cursor.fetchall()
    for row in myresult:
        print(row)

        tree.insert("", tk.END, values=row)
    db.close()
root = tk.Tk()
root.geometry("800x500")
root.maxsize(800, 500)
root.minsize(800, 500)
root.title("NeAM Projects")

lblfrstrow = tk.Label(root, text="Project name -", )
lblfrstrow.place(x=50, y=20)

project_name = tk.Entry(root, width=35)
project_name.place(x=150, y=20, width=100)

lblsecrow = tk.Label(root, text="Project number -")
lblsecrow.place(x=50, y=50)

project_number = tk.Entry(root, width=35)
project_number.place(x=150, y=50, width=100)

submitbtn = tk.Button(root, text ="Add project",
                      bg ='blue', command =projectSubmit)
submitbtn.place(x = 150, y = 100, width = 80)

viewpt = tk.Button(root, text ="View projects",
                      bg ='blue', command = viewProjects)
viewpt.place(x = 0, y = 150, width = 80)

view_window = Toplevel(root)
view_window.title = ("View projects")
view_window.geometry = ("300x300")

tree = ttk.Treeview(view_window, column=("c1", "c2", "c3"), show='headings')

tree.column("#1", anchor=tk.CENTER)

tree.heading("#1", text="ID")

tree.column("#2", anchor=tk.CENTER)

tree.heading("#2", text="Project number")

tree.column("#3", anchor=tk.CENTER)

tree.heading("#3", text="Project name")

tree.pack(pady=10)

root.mainloop()