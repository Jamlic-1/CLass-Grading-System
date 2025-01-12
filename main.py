from tkinter import *
from tkinter import messagebox,ttk
import sqlite3
import tkinter as tk

background_colour='light grey'#Store the background colours of the gui
foreground_colour='black'#Store the foreground colours of the gui

#=======================================================================================================================================================
#CREATE DATABASE TABLES
#=======================================================================================================================================================

# Create a connection to the database
conn = sqlite3.connect('school_management.db')
cursor = conn.cursor()

# Create the necessary tables
cursor.execute('''CREATE TABLE IF NOT EXISTS Teacher (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                password TEXT
                
                )''')
# Create the necessary tables
cursor.execute('''CREATE TABLE IF NOT EXISTS Student (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                gender,
                parent TEXT
                
            )''')
cursor.execute('''
          CREATE TABLE IF NOT EXISTS Marks (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              student_id INTEGER,
              math INTEGER,
              english INTEGER,
              science INTEGER,
              history INTEGER,
              geography INTEGER,
              total_marks INTEGER,
              grade TEXT,
              remark TEXT,
              FOREIGN KEY(student_id) REFERENCES Student(id)
          )''')




#=======================================================================================================================================================
#INITIALIZE THE MAIN WINDOW OF THE GRAPHICAL USER INTERFACE
#=======================================================================================================================================================
window = Tk()  # Create the main application window
screen_width = window.winfo_screenwidth()  # Get screen width of the device
screen_height = window.winfo_screenheight()  # Get screen height of the device
window.geometry(f"{screen_width}x{screen_height}+0+0")  # Set the window size to full screen
window.title('School Management System')  # Set the title of the window

#*****************************************************************************************************************************************************
top_bar = Frame(window, bg='green')  # Create a frame for the top bar
top_bar.pack(side="top", fill="x")  # Pack the top bar frame at the top of the window, filling it horizontally
company_name = Label(top_bar, text="ELIMU BORA PRIMARY SCHOOL CLASS EXAM MANAGEMENT SYSTEM", fg='gold', bg='green', font=('Arial', 20,'bold'))# Add a label to the top bar with the company name and custom styling
company_name.pack( padx=10, pady=1)  # Pack the label on the left side with padding

#******************************************************************************************************************************************************
# Lower top bar with module name
lower_top_bar = Frame(window, bg="#ff9999")  # Create a lower top bar with a different background color
lower_top_bar.pack(side="top", fill="x")  # Pack the lower top bar right below the top bar

module_name = Label(lower_top_bar, text="SIGN UP/ LOG IN", bg="#ff9999", fg="blue", font=('Arial', 15,'bold'))
# Add a label showing the current module (MAIN) with specific styling
module_name.pack(side="left", padx=10, pady=1) 

# Outer container frame to house the side bar and main bar
outer_container_frame = Frame(window)  # Create a frame to act as a container for the side and main bar
outer_container_frame.pack(side="top", fill="x")  

sidebar = Frame(outer_container_frame, bg=background_colour)# Create a side bar frame on the left
sidebar.pack(side="left", fill="y")

main_content = Frame(outer_container_frame, bg=background_colour)# Create a main contents frame on the right
main_content.pack(side="right", fill=X, expand=True, padx=5, pady=0)

taskbar = Frame(window, bg='green')  # Create the taskbar frame at the bottom of the window
taskbar.pack(side="top", fill="x")  # Pack the taskbar at the top below everything else

#******************************************************************************************************************************************************
# Adding the group name label info in the taskbar
company_name = Label(taskbar, text='COMPUTER PROGRAMMING GROUP PROJECT', fg='gold', bg='green', font=('Arial', 19,'bold'))                        
company_name.pack( padx=10, pady=1)  # Pack the label 


###################################################################################################################################################################################
#                         COMMONLY USED FUNCTIONS
###################################################################################################################################################################################
# Creating the Error handling Decorator  to catch and handle errors to prevent the app from crushing    
def error_logging_decorator(func):
                          def wrapper(*args, **kwargs):
                                   try:
                                       return func(*args, **kwargs)
                                   except Exception as e:
                                         messagebox.showerror('Error', f'(AN UNEXPECTED ERROR OCCURED!\n {e}')#Display the error message
                          return wrapper


#A Function to clear the main content frame widgets to allow the shifting from one window to another
@error_logging_decorator
def clear_main_content_frame():
       for widget in main_content.winfo_children():
          widget.destroy()

#The function to create the treevew tables with a scrollbar on the right,it is called in the gui setion where the treeview tables are initialized
@error_logging_decorator
def create_treeview_(tree, column_widths, parent):
         # Set column widths
         for col, width in zip(tree['columns'], column_widths):
                   tree.column(col, width=width)
                   tree.heading(col, text=col)       
         # Place the Treeview in the grid
         tree.grid(row=0, column=0, sticky='nsew')  # Stretch in all directions

         # Create vertical scrollbar
         vscrollbar = Scrollbar(parent, orient=VERTICAL, command=tree.yview)
         vscrollbar.grid(row=0, column=1, sticky='ns')  # Stick to top and bottom
         tree.configure(yscrollcommand=vscrollbar.set)

         # Function to toggle item selection on double click
         decorate_treeview(tree)


#The function to decorate the treeview tables, maes the table to have a grey heardings, and have striped rows 
@error_logging_decorator    
def decorate_treeview(tree):            
                 style = ttk.Style()
                 style.theme_use("clam")                 
                 style.configure("Treeview",background="lavender",foreground="black",rowheight=25,fieldbackground="grey",font=('Arial', 12))
                 style.map('Treeview', background=[('selected', 'blue')]) # Change selected color
                 style.configure("Treeview.Heading", font=('Arial', 12, 'bold'),background="grey", foreground="white") # Customize the heading
                 style.map("Treeview.Heading",background=[('active', 'grey')])            
                 tree.tag_configure('evenrow', background='lightblue')# Adding striped rows
                 tree.tag_configure('oddrow', background='lavenderblush')

#This function populates the treeview tables with data  
@error_logging_decorator     
def update_tree_view(tree, data):
                    tree.delete(*tree.get_children())#DELETE THE EXISTING CONTENTS IN THE TREE VIEW
                    for i, row in enumerate(data):
                              tag = 'evenrow' if i % 2 == 0 else 'oddrow'#DETERMINE EVEN AND ODD ROWS
                              tree.insert('', 'end', values=row, tags=(tag,))# INSERT DATA IN THE TREE VIEW
                              
                              
def log_in_page():
    
    #@error_logging_decorator
    def login():
        if (usernameEntry.get()==''or passwordEntry.get()==''):
            messagebox.showerror('Error', 'Fields cant be empty!! User details are required for you to log in')   
        else:
            log_in_teacher(teacher_name=usernameEntry.get(), teacher_password=passwordEntry.get())
    
    @error_logging_decorator          
    def log_in_teacher(teacher_name, teacher_password):
              cursor.execute('''SELECT name, password FROM Teacher WHERE name = ?;''', (teacher_name,))
              user = cursor.fetchone()
              if user:
                  user_name, user_password = user                                   
                  if teacher_password== user_password:
                       messagebox.showinfo("Info", f'You have successfully logged in, Welcome {user_name}')
                       create_a_side_bar_to_contain_the_menu()
                  else:
                     messagebox.showerror('Error', 'Incorrect Username or password') 
              else:
                     messagebox.showerror('Error', 'Incorrect details, no such user in the database') 
    
    @error_logging_decorator                
    def add_teacher_to_database(name, password):                    
                              cursor.execute('''INSERT INTO Teacher (name, password)
                                            VALUES (?, ?)''', (name, password))
                              conn.commit()  # Commit the transaction
                              messagebox.showinfo("Info", f'You have successfully created a new admin/teacher {name} to the database')
                              create_a_side_bar_to_contain_the_menu()
                              
    #@error_logging_decorator
    def create_account():
        
        if (sign_up_username_label_entry.get()==''or sign_up_Password_label_entry.get()=='' or sign_up_Confirm_Password_label_entry.get()=='' ):
            messagebox.showerror('Error', 'Finish up filling the user details')
        elif sign_up_Password_label_entry.get()!=sign_up_Confirm_Password_label_entry.get():
            messagebox.showerror('Error', 'Your password does not match the Confirm Password, please check')
        else:
            add_teacher_to_database(name=sign_up_username_label_entry.get(), password=sign_up_Password_label_entry.get())
    
    inner_container_frame = tk.Frame(outer_container_frame )
    inner_container_frame.pack(pady=198, padx=250)
    login_frame = tk.Frame(inner_container_frame ,bg='lightgreen')
    login_frame.grid(row=0, column=0)

    user_label = tk.Label(login_frame ,font=("comic sans ms",19),bg='lightgreen',text="Username")
    user_label.grid(row=0, column=0, padx=20, pady=20)
    usernameEntry = ttk.Entry(login_frame ,font=("comic sans ms",15))
    usernameEntry.grid(row=0, column=1, padx=20, pady=20)
    user_label = tk.Label(login_frame ,font=("comic sans ms",19),bg='lightgreen',text="Password")
    user_label.grid(row=1, column=0, padx=20, pady=20)
    user_label = tk.Label(login_frame ,font=("comic sans ms",15),bg='lightgreen', fg='lightgreen',text="Password")
    user_label.grid(row=2, column=0, padx=20, pady=20)
    passwordEntry = ttk.Entry(login_frame ,font=("comic sans ms",15))
    passwordEntry.grid(row=1, column=1, padx=20, pady=20)
#
    signup_button=Button(login_frame,text="Log in",font=("algerian",19),activebackground="#fffa66",activeforeground="red",width=15,cursor='hand2',command=login ).grid(row=3, column=0, columnspan=2,padx=20, pady=20)


    signup_frame = tk.Frame(inner_container_frame ,bg="yellowgreen")
    signup_frame.grid(row=0, column=1)
    user_label = tk.Label(signup_frame ,font=("comic sans ms",19),bg="yellowgreen",text="User Name")
    user_label.grid(row=0, column=0, padx=10, pady=1)
    sign_up_username_label_entry = ttk.Entry(signup_frame ,font=("comic sans ms",15))
    sign_up_username_label_entry.grid(row=0, column=1, padx=20, pady=20)

    
    user_label = tk.Label(signup_frame ,font=("comic sans ms",19),bg="yellowgreen",text="Password")
    user_label.grid(row=5, column=0, padx=20, pady=20)

    sign_up_Password_label_entry = ttk.Entry(signup_frame ,font=("comic sans ms",15))
    sign_up_Password_label_entry.grid(row=5, column=1, padx=20, pady=20)

    Confirm_Password_label = tk.Label(signup_frame ,font=("comic sans ms",19),bg="yellowgreen",text="Confirm Password")
    Confirm_Password_label.grid(row=6, column=0, padx=20, pady=20)

    sign_up_Confirm_Password_label_entry = ttk.Entry(signup_frame ,font=("comic sans ms",15))
    sign_up_Confirm_Password_label_entry.grid(row=6, column=1, padx=20, pady=20)

    signup_button=Button(signup_frame,text="Sign up",font=("algerian",19),activebackground="#fffa66",activeforeground="red",width=15,cursor='hand2', command=create_account).grid(row=7, column=0, columnspan=2,padx=20, pady=20)
    

log_in_page()

###################################################################################################################################################################################
#                         GUI FUNCTIONS
###################################################################################################################################################################################
def create_a_side_bar_to_contain_the_menu(): 
                              @error_logging_decorator
                              def side_bar_menu():
                                        sidebar.config(width=400)                
#                                       Sidebar buttons
                                        sidebar_buttons = [
                                             ("Student Details",student_details_management_gui ),
                                             ("Record Marks",record_marks_gui_interface),
                                             ("Performance",view_performance_gui_interface),
                                                            ]
                                        for (text, command) in sidebar_buttons:
                                              button = Button(sidebar, text=text, command=command, bg=background_colour, activebackground=background_colour, activeforeground=foreground_colour, fg=foreground_colour, anchor="w", padx=10, pady=5,borderwidth=0, highlightbackground="white", font=('Arial', 12, 'bold'),cursor='hand2')
                                              button.pack(fill="x", pady=1)
                              side_bar_menu() #Call the side_bar_menu_function
                              student_details_management_gui()#Call the student_details_management_gui_function

def student_details_management_gui():
                    #This function inserts student information to  the Students table in the database                      
                    @error_logging_decorator                
                    def add_student():
                                 selected_item = tree.focus()
                                 if  selected_item: 
                                        messagebox.showerror("Error", "You cannot add a student in the database when you have selected one, deselect first.")    
                                        return#To prevent one to add a student while he has highlighed a row in the treeview 
                                 else:                              
                                      name =student_name_entry.get()
                                      age =student_age_entry.get() 
                                      gender =student_gender_entry.get()
                                      parent = student_parent_entry.get()
                                      cursor.execute('''INSERT INTO Student (name, age, gender, parent)
                                            VALUES (?, ?, ?,  ?)''', (name, age, gender, parent))
                                      conn.commit()  # Commit the transaction
                                      Update_the_out_put_tree()#Refreshes the trreeview data after theuser has added a new student 
                                      clear_student_entries()
                                      messagebox.showinfo("Info", f'You have successfully recorded new student {name} to the database')
                                      
                    @error_logging_decorator
                    #This function inserts student information to  the Students table in the database    
                    def update_student():
                            selected_item = tree.focus()
                            if selected_item:
                                          row = tree.item(selected_item)['values']
                                          student_id= row[0]
                                          name =student_name_entry.get()
                                          age =student_age_entry.get() 
                                          gender =student_gender_entry.get()
                                          parent = student_parent_entry.get()
                                          cursor.execute('''UPDATE Student SET name=?, age=?, gender=?, parent=? WHERE id=?''', (name, age, gender, parent, student_id))
                                          conn.commit()
                                          Update_the_out_put_tree()
                                          clear_student_entries()
                                          messagebox.showinfo("Info", f'You have successfully updated {name} with id number {student_id} information in the database')
                            else:
                                    messagebox.showerror("Error", "Please select a student to Update.") 

                    @error_logging_decorator
                    def delete_student():
                           selected_item = tree.focus()
                           if selected_item:
                                        row = tree.item(selected_item)['values']
                                        student_id= row[0]
                                        name=row[1]
                                        cursor.execute("DELETE FROM Student WHERE id=?", (student_id,))
                                        conn.commit()  # Commit the transaction
                                        Update_the_out_put_tree()
                                        clear_student_entries()
                                        messagebox.showinfo("Info", f'You have successfully removed {name} with id number {student_id} from the database')
                           else:
                                       messagebox.showerror("Error", "Please select a student to delete from the database.")   

                    @error_logging_decorator
                    def Update_the_out_put_tree():
                               cursor.execute("SELECT * FROM Student")
                               data = cursor.fetchall()  # Fetch all student records
                               update_tree_view(tree, data)

                    @error_logging_decorator
                    def search_student_by_name():
                                               name=student_name_search_entry.get()
                                               cursor = conn.cursor()
                                               # Use a wildcard search to allow partial matches
                                               cursor.execute("SELECT * FROM Student WHERE name LIKE ?", ('%' + name + '%',))
                                               data = cursor.fetchall()  # Fetch all matching records
                                               update_tree_view(tree, data)
                    @error_logging_decorator                       
                    def clear_student_entries():
                                     entries = [student_name_entry, student_age_entry, student_gender_entry, student_parent_entry]
                                     for entry in entries:
                                                  entry.delete(0, 'end')  # Clear each entry field


                    @error_logging_decorator                        
                    def clear():
                               clear_student_entries()   
                               tree.selection_remove(tree.focus())
                               tree.focus('')

                    @error_logging_decorator
                    def display_data(event):
                             selected_item = tree.focus()
                             if selected_item:
                                         row = tree.item(selected_item)['values']
                                         clear_student_entries()
                                         student_name_entry.insert(0, row[1])
                                         student_age_entry.insert(0, row[2])
                                         student_gender_entry.insert(0, row[3])
                                         student_parent_entry.insert(0, row[4])

                           
                    #================================================================================================================================================
                    # GRAPHICAL USER INTERFACE/ FRONTEND
                    #================================================================================================================================================
                    clear_main_content_frame()
                    module_name.config(text='STUDENT MANAGEMENT PAGE') 

                    labelframe=LabelFrame(main_content, bg=background_colour)
                    labelframe.pack(fill=X)

                    student_name_search_entry = ttk.Entry(labelframe, font=('Arial', 12, 'bold'), width=130)
                    student_name_search_entry.grid(row=0, column=0, padx=10, pady=10)

                    clear_button = Button(labelframe, text='🔍Search ', font=('arial',15,'bold'),bg='grey',fg='white',activebackground='grey',activeforeground='white',cursor='hand2',command=search_student_by_name)
                    clear_button.grid(row=0, column=1, padx=1, pady=5)


                    # Treeview
                    treeviewframe=Frame(main_content, bg=background_colour) 
                    treeviewframe.pack(fill=X, padx=10, pady=0)
                    tree = ttk.Treeview(treeviewframe, columns=('ID', 'STUDENT NAME', 'AGE', 'GENDER','GUARDIAN'), show='headings', selectmode='browse', height=21)
                    tree.grid(row=0, column=0)
                    column_widths = [100, 472, 200, 300, 261]
                    create_treeview_(tree, column_widths,parent=treeviewframe)   
                    tree.bind('<ButtonRelease>', display_data)


                    frame = Frame(main_content,bg=background_colour)
                    frame.pack(fill=X)

                # Student Details
                    labelframe=LabelFrame(frame, bg=background_colour)
                    labelframe.grid(row=0,column=0)

                    name_label = Label(labelframe, text='NAME:',font=('Arial', 12, 'bold'), bg=background_colour, fg=foreground_colour)
                    name_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

                    student_name_entry = ttk.Entry(labelframe, font=('Arial', 12, 'bold'))
                    student_name_entry.grid(row=0, column=1, padx=10, pady=10)

                    student_age_label = Label(labelframe, text='AGE:', font=('Arial', 12, 'bold'), bg=background_colour, fg=foreground_colour)
                    student_age_label.grid(row=0, column=2, padx=20, pady=10, sticky='w')

                    student_age_entry= ttk.Entry(labelframe, font=('Arial', 12, 'bold'))
                    student_age_entry.grid(row=0, column=3, padx=15, pady=10)

                    headteacher_label = Label(labelframe, text='GENDER:', font=('Arial', 12, 'bold'), bg=background_colour, fg=foreground_colour)
                    headteacher_label.grid(row=0, column=4, padx=15, pady=10, sticky='w')

                    student_gender_entry= ttk.Entry(labelframe, font=('Arial', 12, 'bold'))
                    student_gender_entry.grid(row=0, column=5, padx=15, pady=10)

                    phone_label = Label(labelframe, text='PARENT:', font=('Arial', 12, 'bold'), bg=background_colour, fg=foreground_colour)
                    phone_label.grid(row=1, column=0, padx=15, pady=10, sticky='w')

                    student_parent_entry = ttk.Entry(labelframe, font=('Arial', 12, 'bold'))
                    student_parent_entry.grid(row=1, column=1, padx=15, pady=10)

                   # Buttons
                    add_button = Button(labelframe, text=' ADD STUDENT ', font=('arial',15,'bold'),bg='blue',fg='white',width=16,activebackground='blue',activeforeground='white'
                                    ,cursor='hand2', command=add_student)
                    add_button.grid(row=1, column=4, padx=3, pady=5)

                    update_button = Button(labelframe, text=' UPDATE ', font=('arial',15,'bold'),bg='green',fg='white',width=16,activebackground='green',activeforeground='white'
                                    ,cursor='hand2', command=update_student)
                    update_button.grid(row=1, column=5, padx=3, pady=5)

                    clear_button = Button(labelframe, text=' CLEAR ', font=('arial',15,'bold'),bg='green',fg='white',width=20,activebackground='green',activeforeground='white'
                                    ,cursor='hand2', command=clear)
                    clear_button.grid(row=1, column=6, padx=3, pady=5)

                    delete_button = Button(labelframe, text=' DELETE ', font=('arial',15,'bold'),bg='red',fg='white',width=20,activebackground='cornflowerblue',activeforeground='white'
                                    ,cursor='hand2', command=delete_student)
                    delete_button.grid(row=0, column=6, padx=3, pady=5)
                    Update_the_out_put_tree()

def record_marks_gui_interface():
                           @error_logging_decorator
                           def grade_student_score(average_score):
                                  if average_score >= 70:
                                             return 'A', 'Excellent'
                                  elif average_score >= 60:
                                              return 'B', 'Good'
                                  elif average_score >= 50:
                                                return 'C', 'Average'
                                  elif average_score >= 40:
                                                return 'D', 'Below Average'
                                  else:
                                         return 'E', 'Poor'

                           # Function to insert student marks
                           @error_logging_decorator        
                           def enter_marks():
                                       selected_item = tree.focus()
                                       if selected_item:
                                             row = tree.item(selected_item)['values']
                                             student_id=row[1]
                                             name=name_entry.get()
                                             math=math_label_entry.get()
                                             english=english_label_entry.get()
                                             science=scence_label_entry.get()
                                             history=history_label_entry.get()
                                             geography=geography_label_entry.get()

                                             # Initialize total_marks
                                             total_marks = 0
                                             subjects = [math, english, science, history, geography]
                                             subject_scores = []

                                             for subject in subjects:
                                                    try:
                                                         if subject:
                                                                 score = int(subject)
                                                                 subject_scores.append(score)
                                                                 total_marks += score
                                                         else:
                                                              subject_scores.append(0)
                                                    except ValueError:
                                                            subject_scores.append(0)  # Default to 0 for invalid input

                                              # Calculate average
                                             average_score = total_marks / 5

                                             grade, remark = grade_student_score(average_score)

                                             cursor.execute('''UPDATE Marks SET math = ?, english = ?, science = ?, history = ?, geography = ?, total_marks = ?, grade = ?, remark = ?
                                                              WHERE student_id = ?''', (math, english, science, history, geography, total_marks, grade, remark, student_id))
                                             conn.commit()
                                             Update_the_out_put_tree()
                                             clear_mark_entering_entries()
                                       else:
                                               pass    



                           # Function to delete student marks
                           @error_logging_decorator             
                           def delete_marks():
                                   selected_item = tree.focus()
                                   if selected_item:
                                          row = tree.item(selected_item)['values']
                                          student_id=row[1]
                                          cursor.execute('''
                                                 UPDATE Marks SET math = ?, english = ?, science = ?, history = ?, geography = ?, total_marks = ?, grade = ?, remark = ?
                                                 WHERE student_id = ?''', (0, 0, 0, 0, 0, 0, 'X', 'No Marks Entered', student_id))
                                          conn.commit()
                                          Update_the_out_put_tree()

                           @error_logging_decorator
                           def load_students_to_enter_marks():
                                         cursor.execute("DELETE FROM Marks")    
                                         cursor.execute("SELECT id FROM Student")
                                         student_ids = cursor.fetchall()

                                         if not student_ids:             
                                                 return

                                         for (student_id,) in student_ids:
                                                   cursor.execute('''INSERT INTO Marks (student_id, math, english, science, history, geography, total_marks, grade, remark)
                                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                                                   (student_id, 0, 0, 0, 0, 0, 0, 'X', 'No Marks Entered'))

                                                   conn.commit()
                                         Update_the_out_put_tree()

                           @error_logging_decorator        
                           def clear_mark_entering_entries():
                                          entries = [name_entry, math_label_entry, english_label_entry, scence_label_entry, history_label_entry, geography_label_entry]
                                          for entry in entries:
                                                     entry.delete(0, 'end')  # Clear each entry field
                           @error_logging_decorator                        
                           def clear():
                                       clear_mark_entering_entries()   
                                       tree.selection_remove(tree.focus())
                                       tree.focus('')

                           @error_logging_decorator
                           def display_data(event):
                                       selected_item = tree.focus()
                                       if selected_item:
                                                  row = tree.item(selected_item)['values']
                                                  clear_mark_entering_entries()
                                                  name_entry.insert(0, row[2])
                                                  math_label_entry.insert(0, row[3])
                                                  english_label_entry.insert(0, row[4])
                                                  scence_label_entry.insert(0, row[5])
                                                  history_label_entry.insert(0, row[6])
                                                  geography_label_entry.insert(0, row[7])

                           @error_logging_decorator
                           def Update_the_out_put_tree():
                                            # Execute a SQL query to fetch the required fields by joining the Marks and Student tables
                                             cursor.execute('''
                                                 SELECT Marks.id,Marks.student_id,Student.name,Marks.math,Marks.english, Marks.science,Marks.history,Marks.geography,Marks.total_marks,Marks.grade,Marks.remark
                                                 FROM  Marks JOIN Student ON Marks.student_id = Student.id  ''')    
                                             data = cursor.fetchall()  # Fetch all records
                                             update_tree_view(tree, data)  # Update the tree view with the fetched data

                           #================================================================================================================================================
                           # BACKEND
                           clear_main_content_frame()
                           module_name.config(text='EXAM MANAGEMENT PAGE                   RECORD EXAM MARKS') 

                           exam_page_status_bar = Label(main_content, text='RECORD EXAM MARKS ',bg='darkred',font=('Arial', 18, 'bold'), fg='white')
                           exam_page_status_bar.pack(fill=X, padx=10, pady=0)

                           #************************************************************************************************************************************
                           #TREEVIEW THAT INCLUDES THE TABLE IN THE SECTION TO INPUT STUDENT MARKS  
                           #****************************************************************************************************************    
                           treeviewframe=Frame(main_content, bg=background_colour) #Frame to contain the treeview table
                           treeviewframe.pack(fill=X, padx=10, pady=0)
                           #Treeview table 
                           tree = ttk.Treeview(treeviewframe, columns=('ID', 'STD_ID', 'STD NAME', 'MATH', 'ENGLISH', 'SCIENCE', 'HISTORY', 'GEOGRAPHY', 'TOTAL MKS', 'GRADE', 'REMARK'  ), show='headings', selectmode='browse', height=22)
                           tree.grid(row=0, column=1)
                           column_widths = [100, 100, 265, 100, 100, 100, 100, 115, 110, 100, 150]#Specify the widths of the tree view table columns
                           create_treeview_(tree, column_widths,parent=treeviewframe) #Call the function to create a table to display the data, and make a scrollbar    
                           tree.bind('<ButtonRelease>', display_data)#Bind Button release to the display data function.This enables the row contents to be diplayed in the entries once user clicks a row

                           frame = Frame(main_content,bg=background_colour)#
                           frame.pack(fill=X)

                           #CREATE different labels and enties to get user input 
                           labelframe=LabelFrame(frame, bg=background_colour)
                           labelframe.grid(row=0,column=0)

                           name_label = Label(labelframe, text='NAME:',font=('Arial', 12, 'bold'), bg=background_colour, fg=foreground_colour)
                           name_label.grid(row=0, column=0, padx=4, pady=5, sticky='w')

                           name_entry = ttk.Entry(labelframe, font=('Arial', 12, 'bold'))
                           name_entry.grid(row=0, column=1, padx=4, pady=5)

                           math_label = Label(labelframe, text='MATH:', font=('Arial', 12, 'bold'), bg=background_colour, fg=foreground_colour)
                           math_label.grid(row=0, column=2, padx=4, pady=5, sticky='w')

                           math_label_entry= ttk.Entry(labelframe, font=('Arial', 12, 'bold'))
                           math_label_entry.grid(row=0, column=3, padx=4, pady=5)

                           english_label = Label(labelframe, text='ENGLISH:', font=('Arial', 12, 'bold'), bg=background_colour, fg=foreground_colour)
                           english_label.grid(row=0, column=4, padx=4, pady=5, sticky='w')

                           english_label_entry= ttk.Entry(labelframe, font=('Arial', 12, 'bold'))
                           english_label_entry.grid(row=0, column=5, padx=4, pady=5)

                           scence_label = Label(labelframe, text='SCIENCE', font=('Arial', 12, 'bold'), bg=background_colour, fg=foreground_colour)
                           scence_label.grid(row=1, column=0, padx=4, pady=5, sticky='w')

                           scence_label_entry = ttk.Entry(labelframe, font=('Arial', 12, 'bold'))
                           scence_label_entry.grid(row=1, column=1, padx=4, pady=5)

                           history_label = Label(labelframe, text='HISTORY', font=('Arial', 12, 'bold'), bg=background_colour, fg=foreground_colour)
                           history_label.grid(row=1, column=2, padx=4, pady=5, sticky='w')

                           history_label_entry = ttk.Entry(labelframe, font=('Arial', 12, 'bold'))
                           history_label_entry.grid(row=1, column=3, padx=4, pady=5)

                           geography_label = Label(labelframe, text='GEOGRAPHY', font=('Arial', 12, 'bold'), bg=background_colour, fg=foreground_colour)
                           geography_label.grid(row=1, column=4, padx=4, pady=5, sticky='w')

                           geography_label_entry = ttk.Entry(labelframe, font=('Arial', 12, 'bold'))
                           geography_label_entry.grid(row=1, column=5, padx=4, pady=5)

                          # Buttons
                           upload_students_button = Button(labelframe, text=' UPLOAD STUDENTS ', font=('arial',14,'bold'),bg='blue',fg='white',width=19,activebackground='blue',activeforeground='white'
                                      ,cursor='hand2', command=load_students_to_enter_marks)
                           upload_students_button.grid(row=0, column=6, padx=5, pady=5)

                           update_button = Button(labelframe, text=' RECORD/UPDATE MKS ', font=('arial',14,'bold'),bg='green',fg='white',width=19,activebackground='green',activeforeground='white'
                                                ,cursor='hand2', command=enter_marks)
                           update_button.grid(row=0, column=7, padx=5, pady=5)

                           delete_button = Button(labelframe, text=' DELETE MKS ', font=('arial',14,'bold'),bg='green',fg='white',width=19,activebackground='green',activeforeground='white'
                                               ,cursor='hand2', command=delete_marks)
                           delete_button.grid(row=1, column=6, padx=5, pady=5)

                           clear_button = Button(labelframe, text=' CLEAR ', font=('arial',14,'bold'),bg='red',fg='white',width=19,activebackground='cornflowerblue',activeforeground='white'
                                          ,cursor='hand2', command=clear)
                           clear_button.grid(row=1, column=7, padx=5, pady=5)
                           Update_the_out_put_tree()


#=======================================================================================================================================================
#THE GRAPHICAL USER INTERFACE TO VIEW SUDENT PERFORMANCE
#=======================================================================================================================================================
def view_performance_gui_interface():

                                @error_logging_decorator
                                def get_student_positions():
                                               cursor.execute('''SELECT Student.id, Student.name, Marks.math, Marks.english, Marks.science,
                                                     Marks.history, Marks.geography, Marks.total_marks, Marks.grade, Marks.remark
                                                    FROM Student
                                                    INNER JOIN Marks ON Student.id = Marks.student_id
                                                       ORDER BY Marks.total_marks DESC''')
                                               return [(i+1, *row) for i, row in enumerate(cursor.fetchall())]

                                @error_logging_decorator
                                def Update_the_out_put_tree():              
                                             data = get_student_positions()
                                             update_tree_view(tree, data)  # Update the tree view with the fetched data

                                @error_logging_decorator          
                                def calculate_class_average_and_subject_averages():
                                                 # Connect to SQLite database
                                                 conn = sqlite3.connect('school_management.db')
                                                 cursor = conn.cursor()

                                                 # Calculate class average by taking the average of total marks
                                                 cursor.execute('SELECT AVG(total_marks) FROM Marks')
                                                 class_avg = cursor.fetchone()[0]

                                                 # Calculate subject averages
                                                 cursor.execute('SELECT AVG(math), AVG(english), AVG(science), AVG(history), AVG(geography) FROM Marks')
                                                 subject_averages = cursor.fetchone()
                                                 class_average_mark_label.config(text=class_avg)
                                                 math_average_mark_label.config(text=subject_averages[0])
                                                 english_average_mark_label.config(text=subject_averages[1])
                                                 science_average_mark_label.config(text=subject_averages[2])
                                                 history_average_mark_label.config(text=subject_averages[3])
                                                 geography_average_mark_label.config(text=subject_averages[4])


                               #================================================================================================================================================
                               #Gui interface for the view performance
                                #__________________________________________________________________________________________________________________________________           
                                clear_main_content_frame()
                                module_name.config(text='EXAM MANAGEMENT PAGE        VIEW STUDENT PERFORMANCE') 

                                exam_page_status_bar = Label(main_content, text='VIEW STUDENT PERFORMANCE ',bg='indigo',font=('Arial', 18, 'bold'), fg='white')
                                exam_page_status_bar.pack(fill=X, padx=10, pady=0)

                               #************************************************************************************************************************************
                               #TREEVIEW THAT INCLUDES THE TABLE IN THE SECTION TO VIEW STUDENT PERFORMANCE  
                               #****************************************************************************************************************      
                                treeviewframe=Frame(main_content, bg=background_colour) 
                                treeviewframe.pack(fill=X, padx=10, pady=0)
                                tree = ttk.Treeview(treeviewframe, columns=('POSITION', 'STD ID','STD NAME', 'MATH', 'ENGLISH', 'SCIENCE', 'HISTORY', 'GEOGRAPHY', 'TOTAL MKS', 'GRADE', 'REMARK'  ), show='headings', selectmode='browse', height=23)
                                tree.grid(row=0, column=0)
                                column_widths = [100,100, 255, 100, 100, 100, 100, 115, 110, 100, 160]
                                create_treeview_(tree, column_widths,parent=treeviewframe) #Call the function to create a table to display the data, and make a scrollbar  

                                frame = Frame(main_content,bg=background_colour)
                                frame.pack(fill=X)

                                # Labels to display the class averages and subject averages in te student performance window
                                labelframe=LabelFrame(frame, bg=background_colour)
                                labelframe.grid(row=0,column=0)

                                class_average_label = Label(labelframe, text='CLASS AVERAGE:',font=('Arial', 12, 'bold'), bg=background_colour, fg=foreground_colour)
                                class_average_label.grid(row=0, column=0, padx=27, pady=5, sticky='w')

                                class_average_mark_label = Label(labelframe, text='',font=('Arial', 12, 'bold'), bg=background_colour, fg='darkred')
                                class_average_mark_label.grid(row=0, column=1, padx=27, pady=5, sticky='w')

                                math_average_label = Label(labelframe, text='MATH AVERAGE:', font=('Arial', 12, 'bold'), bg=background_colour, fg=foreground_colour)
                                math_average_label.grid(row=0, column=2, padx=27, pady=5, sticky='w')

                                math_average_mark_label= Label(labelframe, text='',font=('Arial', 12, 'bold'), bg=background_colour, fg='darkred')
                                math_average_mark_label.grid(row=0, column=3, padx=27, pady=5, sticky='w')

                                english_average_label = Label(labelframe, text='ENGLISH AVERAGE:', font=('Arial', 12, 'bold'), bg=background_colour, fg=foreground_colour)
                                english_average_label.grid(row=0, column=4, padx=27, pady=5, sticky='w')

                                english_average_mark_label = Label(labelframe, text='',font=('Arial', 12, 'bold'), bg=background_colour, fg='darkred')
                                english_average_mark_label.grid(row=0, column=5, padx=27, pady=5, sticky='w')

                                science_average_label = Label(labelframe, text='SCIENCE AVERAGE', font=('Arial', 12, 'bold'), bg=background_colour, fg=foreground_colour)
                                science_average_label.grid(row=1, column=0, padx=27, pady=5, sticky='w')

                                science_average_mark_label = Label(labelframe, text='',font=('Arial', 12, 'bold'), bg=background_colour, fg='darkred')
                                science_average_mark_label.grid(row=1, column=1, padx=27, pady=5, sticky='w')

                                history_average_label = Label(labelframe, text='HISTORY AVERAGE', font=('Arial', 12, 'bold'), bg=background_colour, fg=foreground_colour)
                                history_average_label.grid(row=1, column=2, padx=20, pady=5, sticky='w')

                                history_average_mark_label = Label(labelframe, text='',font=('Arial', 12, 'bold'), bg=background_colour, fg='darkred')
                                history_average_mark_label.grid(row=1, column=3, padx=27, pady=5, sticky='w')

                                geography_average_label = Label(labelframe, text='GEOGRAPHY AVERAGE', font=('Arial', 12, 'bold'), bg=background_colour, fg=foreground_colour)
                                geography_average_label.grid(row=1, column=4, padx=20, pady=5, sticky='w')

                                geography_average_mark_label = Label(labelframe, text='',font=('Arial', 12, 'bold'), bg=background_colour, fg='darkred')
                                geography_average_mark_label.grid(row=1, column=5, padx=27, pady=5, sticky='w')

                                Update_the_out_put_tree()#Call function to populate the student performance display table
                                calculate_class_average_and_subject_averages()#Call function to calculate the class average and the subject averages



window.mainloop()

