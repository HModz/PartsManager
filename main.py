import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import mysql.connector
import pymysql
from sqlalchemy import create_engine

from customtkinter import *
from customtkinter import CTk

import pandas

DB_PASSWORD = os.environ['mysql_db_password']


def connect_to_db():
    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 password=DB_PASSWORD,
                                 db="Neam")
    return db


def get_selected_project():
    selected_project = tree.focus()
    selected_project_details = tree.item(selected_project)
    return selected_project_details


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
            show_projects()
        else:
            pass


def show_projects():
    for i in tree.get_children():
        tree.delete(i)
    db = connect_to_db()
    cursor = db.cursor()
    sql = "SELECT * FROM projects"

    cursor.execute(sql)
    projects = cursor.fetchall()
    for row in projects:
        tree.insert("", tk.END, values=row)
    db.close()


def delete_project():
    selected_project = get_selected_project()
    id = selected_project["values"][0]
    yes = messagebox.askokcancel(title="Warning", message="Are you sure to delete this project?")
    if yes:
        db = connect_to_db()
        cursor = db.cursor()

        sql = f"DELETE FROM projects WHERE ID = {id}"

        cursor.execute(sql)
        db.commit()
        db.close()
        show_projects()


def edit_project_window():
    selected_project = get_selected_project()
    if selected_project["values"] == "":
        messagebox.showerror(title="Error", message="PLEASE SELECT PROJECT TO EDIT!")
    else:
        edit_window = CTkToplevel(window)
        edit_window.title("Edit project")
        edit_window.config(pady=20, padx=20)

        def edit_project():
            id = selected_project["values"][0]
            project_number = project_nmbr_entr.get()
            project_name = project_name_entr.get()
            yes = messagebox.askokcancel(title="Warning", message="Are you sure to proceed?")
            if yes:
                db = connect_to_db()
                cursor = db.cursor()
                sql = f"UPDATE projects SET project_number = %s, project_name = %s WHERE id = {id}"
                val = (project_name, project_number)
                cursor.execute(sql, val)
                db.commit()
                db.close()
                edit_window.destroy()
                show_projects()

        def cancel_edit():
            edit_window.destroy()

        project_nmbr_lbl = CTkLabel(master=edit_window, text="Project number: ")
        project_nmbr_lbl.grid(column=0, row=0)
        project_nmbr_entr = CTkEntry(master=edit_window)
        project_nmbr_entr.insert(0, selected_project["values"][1])
        project_nmbr_entr.grid(column=1, row=0)

        project_name_lbl = CTkLabel(master=edit_window, text="Project name: ")
        project_name_lbl.grid(column=0, row=1)
        project_name_entr = CTkEntry(master=edit_window)
        project_name_entr.insert(0, selected_project["values"][2])
        project_name_entr.grid(column=1, row=1)

        apply_btn = CTkButton(master=edit_window, text="Apply", command=edit_project)
        apply_btn.grid(column=0, row=2, pady=20, padx=20)

        cancel_btn = CTkButton(master=edit_window, text="Cancel", command=cancel_edit)
        cancel_btn.grid(column=1, row=2, pady=20, padx=20)

        edit_window.focus_set()
        edit_window.grab_set()

        edit_window.mainloop()


def login_page():
    login_window = CTkToplevel(window)
    login_window.title("Login")
    login_window.config(padx=20, pady=20)

    user_lbl = CTkLabel(master=login_window, text="User: ")
    user_lbl.grid(column=0, row=0)
    password_lbl = CTkLabel(master=login_window, text="Password: ")
    password_lbl.grid(column=0, row=1)

    login_window.focus_set()
    login_window.grab_set()

    #login_window.mainloop()

def select_project(event):
    selected_project = get_selected_project()
    id = selected_project["values"][0]
    project_name = selected_project["values"][1]

    parts_window = CTkToplevel()
    parts_window.title(f"{project_name}")

    import_btn = CTkButton(master=parts_window, text="Import parts from BOM", command=import_parts)
    import_btn.grid(column=0, row=1, pady=20)

    parts_tree = ttk.Treeview(parts_window, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show='headings')
    parts_tree.column("#1", anchor=tk.CENTER)
    parts_tree.heading("#1", text="Part name")

    parts_tree.column("#2", anchor=tk.CENTER)
    parts_tree.heading("#2", text="Part number")

    parts_tree.column("#3", anchor=tk.CENTER)
    parts_tree.heading("#3", text="Qty")

    parts_tree.column("#4", anchor=tk.CENTER)
    parts_tree.heading("#4", text="Manufacturer")

    parts_tree.column("#5", anchor=tk.CENTER)
    parts_tree.heading("#5", text="Part type")

    parts_tree.column("#6", anchor=tk.CENTER)
    parts_tree.heading("#6", text="Technology")

    parts_tree.column("#7", anchor=tk.CENTER)
    parts_tree.heading("#7", text="Status")
    parts_tree.grid(column=0, row=0)

    parts_window.focus_set()
    parts_window.grab_set()

    for i in parts_tree.get_children():
        parts_tree.delete(i)
    db = connect_to_db()
    cursor = db.cursor()
    sql = "SELECT part_name, part_number, qty, manufacturer, part_type, technology, status FROM parts WHERE project_id = %s"

    cursor.execute(sql, (id,))
    parts = cursor.fetchall()
    for row in parts:
        parts_tree.insert("", tk.END, values=row)
    db.close()

    parts_tree.mainloop()

def import_parts():
    selected_project = get_selected_project()
    id = selected_project["values"][0]
    print(id)

    db = create_engine(f'mysql+pymysql://root:{DB_PASSWORD}@localhost:3306/Neam', echo=False)

    file_path = filedialog.askopenfilename()
    data = pandas.read_excel(io=file_path, skiprows=3)
    data.columns = data.iloc[0]
    data = data[1:]
    clean_data = data.drop(data.columns[[0,3,4,5,10,11,12]], axis=1)
    clean_data.insert(0, 'project_id', id)
    clean_data.rename(columns={'PART NAME': 'part_name', 'PART NUMBER / ORDER NUMBER': 'part_number',
                               'QTY': 'qty', 'MANUFACTURER': 'manufacturer', 'PART TYPE': 'part_type',
                               'TECHNOLOGY': 'technology', 'STATUS': 'status'}, inplace=True)
    print(clean_data)

    clean_data.to_sql(name="parts", con=db, if_exists="append", index=False, chunksize=100)



window = CTk()
window.title("Neam")
window.config(padx=50, pady=50)

#login_page()

project_nmbr_lbl = CTkLabel(master=window, text="Project number: ")
project_nmbr_lbl.grid(column=0, row=0)
project_nmbr_entr = CTkEntry(master=window)
project_nmbr_entr.grid(column=1, row=0)

project_name_lbl = CTkLabel(master=window, text="Project name: ")
project_name_lbl.grid(column=0, row=1)
project_name_entr = CTkEntry(master=window)
project_name_entr.grid(column=1, row=1)

add_project_btn = CTkButton(master=window, text="Add new project", command=add_project)
add_project_btn.grid(column=1, row=3, pady=10)

show_projects_btn = CTkButton(master=window, text="Refresh list", command=show_projects)
show_projects_btn.grid(column=0, row=4)

delete_project_btn = CTkButton(master=window, text="Delete project", command=delete_project)
delete_project_btn.grid(column=2, row=4)

edit_project_btn = CTkButton(master=window, text="Edit project", command=edit_project_window)
edit_project_btn.grid(column=1, row=4)

tree = ttk.Treeview(window, column=("c1", "c2", "c3"), show='headings')
tree.column("#1", anchor=tk.CENTER)
tree.heading("#1", text="ID")
tree.column("#2", anchor=tk.CENTER)
tree.heading("#2", text="Project number")
tree.column("#3", anchor=tk.CENTER)
tree.heading("#3", text="Project name")
tree.grid(column=0, row=5, columnspan=3)
tree.bind("<Double-1>", select_project)

window.mainloop()
