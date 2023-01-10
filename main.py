from tkinter import *
import os
import mysql.connector
from tkinter import messagebox

DB_PASSWORD=os.environ['mysql_db_password']

def connect_to_db():
    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 password=DB_PASSWORD,
                                 db="Neam")
    return db

def add_project():
    project_number = project_nmbr_entr.get()
    project_name = project_name_entr.get()

    if len(project_name) == 0 or len(project_number) == 0:
        messagebox.showerror(title="Error", message="Please insert project number and name!")
    else:
        is_ok = messagebox.askokcancel(title="Check entry", message=f"You want add:\n"
                                                                    f"Project number: {project_number}\n"
                                                                    f"Project name: {project_name}\n"
                                                                    f"Is it ok?")
        if is_ok:
            db = connect_to_db()
            cursor = db.cursor()
            sql = "INSERT INTO projects (project_name, project_number) VALUES (%s, %s)"
            val = (project_name, project_number)
            cursor.execute(sql, val)
            db.commit()
            db.close()
        else:
            pass



window = Tk()
window.title("Neam")
window.config(padx=50, pady=50)

project_nmbr_lbl = Label(text="Project number: ")
project_nmbr_lbl.grid(column=0, row=0)
project_nmbr_entr = Entry()
project_nmbr_entr.grid(column=1, row=0)

project_name_lbl = Label(text="Project name: ")
project_name_lbl.grid(column=0, row=1)
project_name_entr = Entry()
project_name_entr.grid(column=1, row=1)

add_project_btn = Button(text="Add project", command=add_project)
add_project_btn.grid(column=1, row=3)

window.mainloop()
