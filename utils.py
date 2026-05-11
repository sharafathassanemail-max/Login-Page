import pandas as pd
import os
import re #regular expression
from datetime import datetime


CSV_FILE = "user_data.csv"


#initilaizing csv file with columns 

def init_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["user_id","full_name","email","phone","password","registration_date","last_login"])
        df.to_csv(CSV_FILE, index = False)


#validation Functions

def validate_email(email):
    """Email Validation Usinfg Regex"""

    pattern =r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(pattern,email):
        return True,"valid Email "
    return False, "Invalid Email Formate i.e user@domain.com"

def validate_phone(phone):
    """Phone Validate for Pakistani number Formate"""
    #removing spaces and dashes from phone number

    phone = re.sub(r'[\s\-]','',phone)

    #check different phone formats

    pattern =[
        r'^03[0-9]{9}$', #03XXXXXXXXXXXX (pakistani mobile)
        r'^3[0-9]{9}$' , #3XXXXXXXXXXXX
        r'^\+923[0-9]{9}$' #+923XXXXXXXXX
        r'^[0-9]{11}$', #all digit
        r'^00923[0-9]{9}$' #009200000000000
    ]
    
    for pattern in pattern:
        if re.match(pattern,phone):
            return True,"Valid phone Number"
        return False, "Invalid Phone Number"
    

def validate_password(password):
    """password strenght validate"""


    errors=[]


    if len(password)<8:
        errors.append("At least 8 carecters")
    if len(password)>20:
        errors.append("less then 20 careecters")
    if not re.search(r'[A-Z]',password):
        errors.append("at least one upper case letters")
    if not re.search("[a-z]",password):
        errors.append("at least one lower case letters")
    if not re.search(r"[0-9]",password):
        errors.append("at least one number")
    if not re.search(r"[!@#$%^&*]",password):
        errors.append("at one special character (!@#$%^&*)")

    if errors:
        return False, f"password must have: {', '.join(errors)}"
    return True, "Strong Password"

def validate_name(name, field_name="Name"):
    if len(name) < 2:
        return False, f"{field_name} must be at least 2 chareters"
    if len(name) > 50:
        return False, f"{field_name} must be less then 50 charecters"
    if not re.match(r'^[a-zA-z\s\-]+$',name):
        return False, f"{field_name} can only conatains letters, spaces and hyphones"
    return True, f"Valid {field_name}"


def validate_user_id(user_id):
    if len(user_id) < 4:
        return False, f"user id must be at least 4 charecters"
    if len(user_id) > 20:
        return False, f"user id must be less than 20 charecters"
    if not re.match(r"^[a-zA-Z0-9_]+$",user_id):
        return False, "user id can only contains letter, charecters, number and underscore"
    
    #check if user id already exists
    if os.path.exists(CSV_FILE):
        df=pd.read_csv(CSV_FILE)
        if user_id in df["user_id"].values:
            return False, "User ID Already Exists"
    return True, "Valid User Id"

#saving User

def save_user(user_id,full_name,email,phone,password):

    init_csv()

    new_user = pd.DataFrame({
        'new_user' :[user_id],
        'full_name' :[full_name],
        'email' :[email],
        'phone' :[phone],
        'password' :[password],
        'registration_date' :[datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        'last_login' :[' ']
    })

    existing_data=pd.read_csv(CSV_FILE)
    update_data=pd.concat([existing_data,new_user],ignore_index = True)
    update_data.to_csv(CSV_FILE,index=False)
    return True

def validate_login(user_id,password):
    """Check if creadentials are correct"""


    init_csv()

    df=pd.read_csv(CSV_FILE)

    #cheack if user exists
    user_data=df[df['user_id']==user_id]

    if len(user_data)==0:
        return False, "User Id Not Found"
    
    #check password as well

    stored_password=user_data.iloc[0]['password']

    if stored_password==password: 
        #updating last login timmings
        df.loc[df['user_id']==user_id, 'last_login']==datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        df.to_csv(CSV_FILE, index=False)
        return True, f"Welcome Back, {user_data.iloc[0]['full_name']}!"
    return False, "Incorrect Password!"

#get user details

def get_user_details(user_id):
    "Get ull details by user Id"
    df=pd.read_csv(CSV_FILE)
    user_data=df[df['user_id']==user_id]
    if len(user_data)>0:
        return user_data.iloc[0].to_dict()
    return None