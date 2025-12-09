from datetime import datetime


MODULE_CONFIGUARTION={}
student_db=[]
def calculate_overall_score(score_list):
   print(MODULE_CONFIGUARTION)
   for student in score_list:
     Overall_score=0
     for key,value in  student['scores'].items():
       Overall_score += int(value) * MODULE_CONFIGUARTION[key]
     student_db.append({student['name']:Overall_score})
   print(student_db)
     
   
  
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