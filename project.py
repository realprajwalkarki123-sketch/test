from datetime import datetime, date
from tabulate import tabulate
import csv

import os
import ast

MODULE_CONFIGUARTION = {}
STUDENT_DB = []
STUDENT_INFO = []
MAIN_FILE = "students.txt"
TABLE_FILE = "student_table.txt"
id_list=[]


def load_previous_students(filename=MAIN_FILE):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        content = f.read().strip()
    try:
        return ast.literal_eval(content)
    except Exception as e:
        print("Something  unexpected happen and fail to load the students")
        return []


def save_table(students, filename=TABLE_FILE):
    table_str = tabulate(get_clean_studentdb(students), headers="keys", tablefmt="grid")
    with open(filename, "w") as f:
        f.write(table_str)


def save_students(DATABASE, filename=MAIN_FILE):
    with open(filename, "w") as f:
        f.write(str(DATABASE))


def get_clean_studentdb(db):
    clean = [{key: value for key, value in d.items() if key != "scores"} for d in db]
    return clean


def round_to_category(score):
    score = float(score)

    # -----------------------------
    # EXTREME CASES
    # -----------------------------
    if score <= 0:
        return 0, "No Submission"
    elif score >= 100:
        return 100, "Gold Standard"

    # -----------------------------
    # FAIL (5, 15, 25)
    # -----------------------------
    if score <= 10:
        return 5, "Fail"
    elif score <= 20:
        return 15, "Fail"
    elif score <= 28:
        return 25, "Fail"

    # -----------------------------
    # CONDONABLE FAIL (32, 35, 38)
    # -----------------------------
    elif score <= 33:
        return 32, "Condonable Fail"
    elif score <= 36:
        return 35, "Condonable Fail"
    elif score <= 40:
        return 38, "Condonable Fail"

    # -----------------------------
    # THIRD (42, 45, 48)
    # -----------------------------
    elif score <= 43:
        return 42, "Third"
    elif score <= 46:
        return 45, "Third"
    elif score <= 50:
        return 48, "Third"

    # -----------------------------
    # LOWER SECOND (52, 55, 58)
    # -----------------------------
    elif score <= 53:
        return 52, "Lower Second"
    elif score <= 56:
        return 55, "Lower Second"
    elif score <= 60:
        return 58, "Lower Second"

    # -----------------------------
    # UPPER SECOND (62, 65, 68)
    # -----------------------------
    elif score <= 63:
        return 62, "Upper Second"
    elif score <= 66:
        return 65, "Upper Second"
    elif score <= 70:
        return 68, "Upper Second"

    # -----------------------------
    # FIRST (72, 75, 78)
    # -----------------------------
    elif score <= 74:
        return 72, "First"
    elif score <= 77:
        return 75, "First"
    elif score <= 80:
        return 78, "First"

    # -----------------------------
    # UPPER FIRST (82, 85, 92)
    # -----------------------------
    elif score <= 83:
        return 82, "Upper First"
    elif score <= 88:
        return 85, "Upper First"
    elif score <= 96:
        return 92, "Upper First"

    # -----------------------------
    # GOLD STANDARD (100 fallback)
    # -----------------------------
    else:
        return 100, "Gold Standard"


def get_student_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    

def calculate_overall_score(score_list):

    for student in score_list:
        Overall_score = 0
        for key, value in student["scores"].items():
            Overall_score += int(value) * MODULE_CONFIGUARTION[key]
            rounded_score, category = round_to_category(Overall_score)
        STUDENT_DB.append(
            {
                **student,
                "raw score": Overall_score,
                "rounded_score": rounded_score,
                "category": category,
            }
        )


def get_valid_score(component):
    while True:
        score = int(input(f"{component} score "))
        if score >= 0 and score <= 100:
            return score  
        if score < 0:
            print("Score must be greater or equal to zero")
        if score > 100:
            print("Score must be less than or equal to 100")


def get_valid_dob():
    while True:
        dob_input = input("Date of Birth (YYYY-MM-DD): ")
        try:
            actual_dob = datetime.strptime(dob_input, "%Y-%m-%d").date()
            today = date.today()
            if actual_dob.year <= today.year:
                return actual_dob
            print("This can't be your correct date of birth")
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM-DD format.")

def check_for_id(id):
    id_list.append(id)
    isPresent=list(filter(lambda x:x==id,id_list))
    if(len(isPresent)>1):
        return True
    data=load_previous_students()
    for student in data:
        if(int(student['UID'])==id):
            return True

def get_valid_id():
    
    while True:
        id = input("Enter ID of the student ")
        
        if  id.upper() == "END":
            return False
        try:
           isPresent=check_for_id(int(id))
           if not isPresent:
               if int(id) < 99 and int(id) > 0:
                   return id
               print("Id must be less than 100 and greater than 0")
           print("Student already exits with the same UID")
        except ValueError:
                 print("Invalid number")
       

def main():

    print(
        "Welcome to the Student Grading System First, let's set up the module configuration. "
    )

    module_name = input("Enter module name ")
    ans = input("Do you want to use the default module configuration(y/n)? ")
    if ans.upper() == "Y":
        default_list = [
            {"name": "Coursework_1", "weight": 0.1},
            {"name": "Coursework_2", "weight": 0.2},
            {"name": "Coursework_3", "weight": 0.3},
            {"name": "final_exam", "weight": 0.4},
        ]
        for item in default_list:
            MODULE_CONFIGUARTION[item["name"]] = item["weight"]
    #  module_name=()

    else:
        no_of_components = int(
            input("How many assessment components does this module have?")
        )
        total_weight=0
        for i in range(1, no_of_components + 1):
            component_name = input(f"Component {i} name: ")
            weight =float(input(f"Component {i} weight(%) "))
            total_weight+=weight
            
            MODULE_CONFIGUARTION[component_name] = weight / 100
        if(total_weight<100):

            print("It should be equal to 100")
            
            return
        
        print("Module configuration complete.")

    print("Now, let's enter student information and grades.")
    
    for i in range(1, 4):
        id = get_valid_id()
        
        if not id:
            break
        name = input("Enter name of the student ")
        dob = get_valid_dob()
        age = get_student_age(dob)
        student_data = {
            "UID": id,
            "name": name,
            "DOB": dob.strftime("%Y-%m-%d"),
            "age": age,
            "scores": {},
        }
        for component in list(MODULE_CONFIGUARTION.keys()):
            score = get_valid_score(component)
            student_data["scores"][component] = score
        STUDENT_INFO.append(student_data)

    calculate_overall_score(STUDENT_INFO)
    previous_students = load_previous_students(MAIN_FILE)
    
    if STUDENT_DB:
        DATABASE = get_clean_studentdb(STUDENT_DB)
    else:
        DATABASE=[]
    COMPLETE_DATABASE=DATABASE+previous_students
    


    
    SORTED_DATABASE = sorted(COMPLETE_DATABASE, key=lambda x: int(x["UID"]))
    table = tabulate(SORTED_DATABASE, headers="keys", tablefmt="fancy_grid")

    save_students(SORTED_DATABASE)
    save_table(SORTED_DATABASE)
    print(table)

def advanced():
    filename = input("Enter the filename: ")

    if not os.path.exists(filename):
        print("File not found.")
        return []

    with open(filename, "r") as f:
        content = f.read().strip()

    headers = ["StudentID", "Name", "DateOfBirth",
               "Coursework_1", "Coursework_2", "Coursework_3", "Coursework_4"]

    students = []

    for line in content.split("\n"):
        if not line.strip():
            continue

        values = line.split(",")
        row = dict(zip(headers, values))

      
        scores_dict = {
            "Coursework_1": int(row["Coursework_1"]),
            "Coursework_2": int(row["Coursework_2"]),
            "Coursework_3": int(row["Coursework_3"]),
            "Coursework_4": int(row["Coursework_4"]),
        }

        student_data = {
            "UID": row["StudentID"],
            "name": row["Name"],
            "DOB": row["DateOfBirth"],
            "age": get_student_age(datetime.strptime(row["DateOfBirth"], "%Y-%m-%d").date()),
            "scores": scores_dict
        }

        students.append(student_data)

  
    MODULE_CONFIGUARTION.clear()
    MODULE_CONFIGUARTION["Coursework_1"] = 0.1
    MODULE_CONFIGUARTION["Coursework_2"] = 0.2
    MODULE_CONFIGUARTION["Coursework_3"] = 0.3
    MODULE_CONFIGUARTION["Coursework_4"] = 0.4

   
    calculate_overall_score(students)

    print("\nImported and Calculated Student Results:\n")
    print(tabulate(get_clean_studentdb(STUDENT_DB), headers="keys", tablefmt="fancy_grid"))
    save_table(get_clean_studentdb(STUDENT_DB))
    save_students(get_clean_studentdb(STUDENT_DB))
    
if __name__ == "__main__":
     ans=int(input("Do you want to manually enter the data or import from file ( 1 for manual and 2 for import)"))
     match ans:
         case 1:
             main()
         case 2:
             advanced()


