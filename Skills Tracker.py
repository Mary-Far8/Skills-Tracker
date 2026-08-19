import sqlite3 
from tkinter import *
from tkinter import messagebox


# connect to (or create) the skills database file
connection = sqlite3.connect("skills.db")
# cursor is the tool used to run SQL commands through the connection
cursor = connection.cursor()



# create the skills table if it doesn't already exist
# id = auto-numbered unique identifier for each row
# name = the skill's name, must be unique (no duplicate skill names allowed)
# progress = a number representing progress on that skill
cursor.execute(
     """CREATE TABLE IF NOT EXISTS skills(
                  id INTEGER PRIMARY KEY,
                 name TEXT UNIQUE,
                  progress INTEGER
                  )

                 """)


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

# inserts a new skill into the database
# if the name already exists (UNIQUE constraint), catches the error instead of crashing
def add_skills() :

    name = skill_name.get()
    progress = progress_value.get()
    
    try:
      #add it to the database
      cursor.execute('INSERT INTO skills (name,progress) VALUES (?, ?)', (name, progress)) 
      # add it to the listbox
      skills_list.insert("end", f"{name} ==> {progress}")

    except sqlite3.IntegrityError :
       print(f"'{name}' already exists — skipping.")
    connection.commit()



def refresh_skills_list():
    skills_list.delete(0, END)
    cursor.execute("SELECT * FROM skills")
    rows = cursor.fetchall()
    for row in rows:
        skill_id, name, progress = row
        skills_list.insert(END, f"{name} ==> {progress}")

# updates an existing skill's progress value
# rowcount == 0 means no skill with that name was found
def update_skills():
    name = skill_name.get()
    new_progress = progress_value.get()
    cursor.execute('UPDATE skills SET progress = ? WHERE name = ?', (new_progress, name))
    if cursor.rowcount == 0:
        messagebox.showerror(message=f"the skill {name} does not exist")
    connection.commit()
    refresh_skills_list()

# deletes a skill from the database by name
# rowcount == 0 means no skill with that name was found
def delete_skills():
    name = skill_name.get()
    cursor.execute('DELETE FROM skills WHERE name = ?', (name,))
    if cursor.rowcount == 0:
        messagebox.showerror(message=f"{name} does not exist")
    connection.commit()
    refresh_skills_list()
   
    connection.commit()

    
      





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




connection.commit()
connection.close()
skills_Tracker.mainloop()