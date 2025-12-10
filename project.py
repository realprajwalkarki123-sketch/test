from datetime import datetime,date
from tabulate import tabulate
import os
import ast
MODULE_CONFIGUARTION={}
STUDENT_DB=[]
STUDENT_INFO=[]
MAIN_FILE="students.txt"
TABLE_FILE="student_table.txt"
def load_previous_students(filename=MAIN_FILE):
   if not os.path.exists(filename):
      return []
   with open(filename,"r") as f:
      content=f.read().strip()
   try:
      return  ast.literal_eval(content)
   except Exception as e:
      print("Something  unexpected happen and fail to load the students")
      return []
def save_table(students, filename=TABLE_FILE):
    table_str = tabulate(get_clean_studentdb(students), headers="keys", tablefmt="grid")
    with open(filename, "w") as f:
        f.write(table_str)
def save_students(DATABASE,filename=MAIN_FILE):
   with open(filename,"w") as f:
      f.write(str(DATABASE))
      
def get_clean_studentdb(db):
   clean=[{key: value for key, value in d.items() if key!= "scores"} for d in db]
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
   today=date.today()
   return today.year - dob.year-((today.month,today.day)<(dob.month,dob.day))
   
def calculate_overall_score(score_list):
   

   for student in score_list:
     Overall_score=0
     for key,value in  student['scores'].items():
       Overall_score += int(value) * MODULE_CONFIGUARTION[key]
       rounded_score,category=round_to_category(Overall_score)
     STUDENT_DB.append({**student,'raw score':Overall_score,'rounded_score':rounded_score,'category':category})
   
   
def get_valid_score(component):
   while True:
      score=int(input(f"{component} score "))
      if(score>=0 and score<=100):
         return score
      if(score<0):
         print("Score must be greater or equal to zero")
      if(score>100):
         print("Score must be less than or equal to 100")
    
   
def get_valid_dob():
   while True:
        dob_input = input("Date of Birth (YYYY-MM-DD): ")
        try:
            actual_dob = datetime.strptime(dob_input, "%Y-%m-%d").date()
            today=date.today()
            if actual_dob.year<=today.year:            
             return actual_dob
            print("This can't be your correct date of birth") 
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM-DD format.")   
   
  
#   print(score_list)
  
def main():

  print("Welcome to the Student Grading System First, let's set up the module configuration. ")

  module_name=input("Enter module name ")
  ans=input("Do you want to use the default module configuration(y/n)? ")
  if(ans.upper()=='Y'):
     default_list=[{'name': 'Coursework_1','weight':0.1},{'name': 'Coursework_2','weight':0.2},{'name': 'Coursework_3','weight':0.3},{'name': 'final_exam','weight':0.4}]
     for item in default_list:
      MODULE_CONFIGUARTION[item['name']]=item['weight']
    #  module_name=()


  else:
    no_of_components=int(input("How many assessment components does this module have?"))
    for i in range(1,no_of_components+1):
      component_name= input(f"Component {i} name: ")
      weight=int(input(f"Component {i} weight(%) "))
      MODULE_CONFIGUARTION[component_name]=weight/100
    print("Module configuration complete.")

    

  print("Now, let's enter student information and grades.")


  for i in range(1,4):
     id=input("Enter student ID ")
     if( id.upper()=="END"):
       break
     name=input("Enter name of the student ")
     dob=get_valid_dob()
     age=get_student_age(dob)
     student_data={'UID':id,'name':name,"DOB":dob.strftime("%Y-%m-%d"),"age":age,"scores":{}}
     for component in list(MODULE_CONFIGUARTION.keys()):
       score=get_valid_score(component)
       student_data['scores'][component]=score
     STUDENT_INFO.append(student_data)


  calculate_overall_score(STUDENT_INFO)
  if(STUDENT_DB):
     DATABASE=get_clean_studentdb(STUDENT_DB)
  previous_students=load_previous_students(MAIN_FILE)
  table=tabulate(previous_students+DATABASE,headers="keys",tablefmt="fancy_grid")
  
  
  save_students(previous_students+DATABASE)
  save_table(previous_students+DATABASE)
  print(table)
  


if __name__=="__main__":
  main()