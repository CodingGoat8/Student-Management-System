

import streamlit as st
import bcrypt
from database import student_collection, user_collection

st.title("Student Management System")


# ---------------- SESSION ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

#------------FUNCTIONS------------
#-------------SignUp-----------------
def SignUp():
    
   st.title("SignUp Here...")

   username = st.text_input("Enter Username: ")
   password = st.text_input(
       "Enter Password",
        type="password"
   )

   if st.button("SignUp"):

       existing_user = user_collection.find_one(
           {"username" : username }

       )

       if existing_user:
           st.warning("Username Already Exists")
    
       else:
           hashed_password = bcrypt.hashpw(
               password.encode("utf-8"),
               bcrypt.gensalt()
           )

           user_data = {
               "username" : username,
               "password" : hashed_password
           }

           user_collection.insert_one(user_data)
           st.success("Signup Successfull")

    


#-------------LogIn---------------
def LogIn():
    st.title("LogIn Here...")

    username = st.text_input("Enter Username: ")
    password = st.text_input(
        "Enter Password",
        type="password"
    )

    if st.button("LogIn"):
        user = user_collection.find_one(
            {"username" : username}
        )

        if user:
            stored_password = user["password"]

            password_correct = bcrypt.checkpw(
                password.encode("utf-8"),
                stored_password
            )

            if password_correct:
                st.session_state.logged_in = True

                st.success("Login Succesfully!")

                st.rerun()
            
            else:
                st.error("Wrong Password")



        else:
            st.error("User Not Found!")    


#-------------Add Student------------          

def Add_Student():

    st.title("Add Student...")   

    with st.form("Add Student"):
        name = st.text_input(
            "Enter Student Name: "
        )

        age = st.number_input(
            "Enter Student Age: ",
             min_value=2,
             max_value=38
        )

        gender = st.radio(
            "Gender", ["Male", "Female"]
        )

        roll = st.text_input(
            "Enter Student Roll no: "
        )

        dept = st.text_input(
            "Enter Student Department: "
        )

        address = st.text_area(
            "Enter Student Address: "
        )

        phone = st.text_input(
            "Enter Students Phone Number: "
        )

        submit = st.form_submit_button(
            "Save Student"
        )

        if submit:

            student_data = {
                "name": name,
                "age" : age,
                "gender": gender,
                "roll" : roll,
                "dept" : dept,
                "address" : address,
                "phone" : phone
            }

            student_collection.insert_one(student_data)
            st.success("Student Added Successfully!")

#-------------Search Student---------------

def Search_Student():
    st.title("Search Student with Roll Number...")            

    search_roll = st.text_input(
        "Enter Student Roll no: "
    )

    if st.button("Search"):

        student = student_collection.find_one(
            {"roll" : search_roll},
            {"_id" : 0}
        )

        if student:
            st.success("Student Found")
            st.json(student)

        else:
            st.error("Student Not Found")


#------------Update Student-----------

def Update_Student():
    st.title("Update Student Here...")

    search_roll = st.text_input("Enter Student Roll: ")

    student = None

    if search_roll:

        student = student_collection.find_one(
            {"roll" : search_roll},
            {"_id" : 0}
        )

        if student:

            with st.form("Updated_Data"):
                Name = st.text_input(
                    "Student Name: ",
                    value=student["name"]
                )

                Age = st.number_input(
                    "Student Age: ",
                    value=student["age"],
                    min_value=2,
                    max_value=38
                )

                Gender = st.radio(
                    "Gender",
                    ["Male", "Female"],
                    index=0 if student["gender"] == "Male" else 1
                )

                

                Dept = st.text_input(
                    "Student Department: ",
                     value=student["dept"]
                )

                Address = st.text_area(
                    "Student Address: ",
                    value=student["address"]
                )

                Phone = st.text_input(
                    "Student Phone: ",
                    value=student["phone"]
                )

                UpdateBtn = st.form_submit_button(
                    "Update Student"
                )

                if UpdateBtn:

                    updated_data = {
                        "name" : Name,
                        "age" : Age,
                        "gender" : Gender,
                        "dept" : Dept,
                        "address" : Address,
                        "phone" : Phone

                    }

                    student_collection.update_one(
                        {"roll" : search_roll},
                        {
                            "$set" : updated_data
                        }

                    )

                    st.success("Student Data Updated")

    elif search_roll:
        st.error("Student Not Found")


#--------Delete Student----------
def Delete_Student():

    st.title("Delete Student here...")

    delete_roll = st.text_input("Enter Roll no to Delete: ")

    if st.button("Delete"):

        result = student_collection.delete_one(
            {"roll" : delete_roll}
        )

        if result.deleted_count > 0:
            st.success("Student Deleted Successfully")

        else:
            st.error("Student Not Found!")    



#-----------View Students------------
def View_Student():

    st.title("All Students")

    AllStudents = list(
        student_collection.find({}, {"_id" : 0})
        )
    
    if AllStudents:
        st.dataframe(AllStudents)

    else:
        st.warning("No Students Found")    




    



#---------------MAIN-----------------

if not st.session_state.logged_in:

    menu = st.sidebar.selectbox(
        "Select Option",
        ["SignUp", "LogIn"]
        
    )

    if menu == "SignUp":
        SignUp()

    elif menu == "LogIn":
        LogIn()

else:
     st.sidebar.success("User Verified")

     menu = st.sidebar.selectbox(
         "Nevigation",
         [
             "Add Student",
             "Search Student",
             "Update Student",
             "Delete Student",
             "View Student"

         ]
     )

     if menu == "Add Student":
         Add_Student()

     elif menu == "Search Student":
         Search_Student()    

     elif menu == "Update Student":
         Update_Student()

     elif menu == "Delete Student":
         Delete_Student()

     elif menu == "View Student":
         View_Student()
     
     if st.sidebar.button("Logout"):
         st.session_state.logged_in = False

         st.rerun()



















