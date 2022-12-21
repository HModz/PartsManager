import tkinter as tk
import mysql.connector
from tkinter import ttk
from tkinter import *
import os


db_password=os.environ['mysql_db_password']



def projectSubmit():
    prname = project_name.get()
    prnumber = project_number.get()

    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 password=db_password,
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
                                 password=db_password,
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

def get_selection():
    selected_project = tree.focus()
    selected_project_details = tree.item(selected_project)

    part_window = Toplevel(root)
    part_window.title = ("View projects")
    part_window.geometry = ("300x300")

    tree_parts = ttk.Treeview(part_window, column=("c1", "c2", "c3", "c4","c5","c6", "c7", "c8"), show='headings')

    tree_parts.column("#1", anchor=tk.CENTER)
    tree_parts.heading("#1", text="Project_ID")

    tree_parts.column("#2", anchor=tk.CENTER)
    tree_parts.heading("#2", text="Part name")

    tree_parts.column("#3", anchor=tk.CENTER)
    tree_parts.heading("#3", text="Part number")

    tree_parts.column("#4", anchor=tk.CENTER)
    tree_parts.heading("#4", text="Qty")

    tree_parts.column("#5", anchor=tk.CENTER)
    tree_parts.heading("#5", text="Manufacturer")

    tree_parts.column("#6", anchor=tk.CENTER)
    tree_parts.heading("#6", text="Part type")

    tree_parts.column("#7", anchor=tk.CENTER)
    tree_parts.heading("#7", text="Technology")

    tree_parts.column("#8", anchor=tk.CENTER)
    tree_parts.heading("#8", text="Status")

    tree_parts.pack()

    def viewParts():
        for i in tree_parts.get_children():
            tree_parts.delete(i)
        db = mysql.connector.connect(host="localhost",
                                     user="root",
                                     password=db_password,
                                     db="Neam")
        cursor = db.cursor()
        sql = "SELECT * FROM parts WHERE project_id = %s"
        id = selected_project_details["values"][0]
        cursor.execute(sql, (id,))
        myresult = cursor.fetchall()
        for row in myresult:
            print(row)

            tree_parts.insert("", tk.END, values=row)
        db.close()
    viewParts()
    part_window.mainloop()

lblfrstrow = tk.Label(root, text="Project name -", )
lblfrstrow.place(x=50, y=20)

project_name = tk.Entry(root, width=35)
project_name.place(x=150, y=20, width=100)

lblsecrow = tk.Label(root, text="Project number -")
lblsecrow.place(x=50, y=50)

project_number = tk.Entry(root, width=35)
project_number.place(x=150, y=50, width=100)

submitbtn = tk.Button(root, text ="Add project",
                      bg ='grey', command =projectSubmit)
submitbtn.place(x = 150, y = 100, width = 80)

viewpt = tk.Button(root, text ="View projects",
                      bg ='grey', command = viewProjects)
viewpt.place(x = 0, y = 150, width = 80)

view_window = Toplevel(root)
view_window.title = ("View projects")
view_window.geometry = ("300x300")

select_project_btn = tk.Button(view_window, text ="Select project",
                      bg ='grey', command = get_selection)
select_project_btn.place(x=500, y=300)
select_project_btn.pack()

tree = ttk.Treeview(view_window, column=("c1", "c2", "c3"), show='headings')

tree.column("#1", anchor=tk.CENTER)

tree.heading("#1", text="ID")

tree.column("#2", anchor=tk.CENTER)

tree.heading("#2", text="Project number")

tree.column("#3", anchor=tk.CENTER)

tree.heading("#3", text="Project name")

tree.pack()



root.mainloop()