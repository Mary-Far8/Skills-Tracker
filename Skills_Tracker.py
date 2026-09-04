from tkinter import *
from tkinter import messagebox
from database import cursor,connection
from skills_service import add_skill_to_db,delete_skills_from_db,get_all_skills,update_skills_in_db



# create the main app window
skills_Tracker = Tk()
skills_Tracker.title("Skills Tracker App")
skills_Tracker.configure(bg="#1D4533") 
skills_Tracker.geometry("600x650")

# heading label at the top of the app
ST_label1= Label(skills_Tracker, text="Add Your Skills", bg="#1D4533", fg="white", font=('Arial',20,'bold'),pady=10)
ST_label1.pack(pady=(40, 0) )
# frame grouping the skill name + progress inputs together
ST_frame = Frame(skills_Tracker, bg="#1D4533")
ST_frame.pack(pady=5)

# label above the skill name entry
ST_frame_labe1 = Label(ST_frame, text="skill", font=('Arial',12,'bold'),bg="#1D4533" ,fg="white")
ST_frame_labe1.pack(anchor='w',pady=5)

# variable bridging the skill name Entry box to Python code
skill_name = StringVar()
skill_name.set("")

# entry box where the user types the skill's name
Skill_Entry = Entry(ST_frame, textvariable=skill_name, font=('Arial', 10, 'bold'), bg='white', fg='black')
Skill_Entry.pack(pady=5)

# label above the progress entry
ST_frame_labe2 = Label(ST_frame, text="progress", font=('Arial',12,'bold'),bg="#1D4533" ,fg="white")
ST_frame_labe2.pack(anchor='w',pady=5)

# variable bridging the progress Entry box to Python code
progress_value =StringVar()
progress_value.set("")

# entry box where the user types the progress value
progress_entry = Entry(ST_frame, textvariable=progress_value,font=('Arial', 10, 'bold'), bg='white', fg='black')
progress_entry.pack(anchor="w", pady=5)




def add_skills():
    name = skill_name.get()
    progress = progress_value.get()
    success = add_skill_to_db(cursor, connection, name, progress) 
    if success:
        skills_list.insert("end", f"{name} ==> {progress}")
    else:
        print(f"'{name}' already exists — skipping.")


def refresh_skills_list():
    skills_list.delete(0, END)
    rows = get_all_skills(cursor)
    for row in rows:
        skill_id, name, progress = row
        skills_list.insert(END, f"{name} ==> {progress}")


def update_skills():
    name = skill_name.get()
    new_progress = progress_value.get()
    success = update_skills_in_db(connection , cursor , name, new_progress)
    if success :
        skills_list.insert("end", f"{name} ==> {new_progress}")
    else :
        messagebox.showerror(message=f"the skill {name} does not exist")
    refresh_skills_list()


def delete_skills():
    name = skill_name.get()
    success = delete_skills_from_db(cursor,connection,name)
    if not success :
        messagebox.showerror(message=f"{name} does not exist")
    connection.commit()
    refresh_skills_list()
   

    
button1 = Button(skills_Tracker, bg="#F7EAE0",fg='black', font=('Arial',12,'bold'),borderwidth=0, text='add skill', command= add_skills)
button2 = Button(skills_Tracker, bg="#F7EAE0",fg='black', font=('Arial',12,'bold'),borderwidth=0, text='update skill', command= update_skills)
button3 = Button(skills_Tracker, bg="#F7EAE0",fg='black', font=('Arial',12,'bold'),borderwidth=0, text='delete skill',command = delete_skills)
button1.pack(pady=10)
button2.pack(pady=10)
button3.pack(pady=10)


button4 = Button(skills_Tracker, bg="#F7EAE0",fg='black', font=('Arial',12,'bold'),borderwidth=0, text='show skills',command = refresh_skills_list)
button4.pack(pady=10)

skills_list = Listbox(skills_Tracker, bg="white", fg='black', font=('Arial',10,'bold'), height=10) 
skills_list.pack(pady=10)


if __name__ == "__main__":
    skills_Tracker.mainloop()
    connection.close()
