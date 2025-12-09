from datetime import datetime


MODULE_CONFIGUARTION={}
student_db=[]

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

def calculate_overall_score(score_list):

   for student in score_list:
     Overall_score=0
     for key,value in  student['scores'].items():
       Overall_score += int(value) * MODULE_CONFIGUARTION[key]
       rounded_score,category=round_to_category(Overall_score)
     student_db.append({student['name']:Overall_score,'rounded_score':rounded_score,'category':category})
    
   
     
   
  
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
  score_list=[]
 
  for i in range(1,4):
     id=input("Enter student ID ")
     if( id=="end" or id=="END"):
       break
     name=input("Enter name of the student ")
     dob=input("Date of Birth (YYYY-MM-DD) ")
     actual_dob=datetime.strptime(dob,"%Y-%m-%d").date()
     student_data={'name':name,"scores":{}}
     for component in list(MODULE_CONFIGUARTION.keys()):
       score=input(f"{component} score")
       student_data['scores'][component]=score
     score_list.append(student_data)


  calculate_overall_score(score_list)



if __name__=="__main__":
  main()