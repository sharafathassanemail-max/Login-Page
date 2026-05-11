#registration App
import streamlit as st
from utils import (
    validate_email,validate_name,validate_login,validate_password,validate_phone,validate_user_id,save_user
)


st.set_page_config(
    page_title="User Registration",
    layout="centered"
)

st.title("User Registration Form")

if 'form_submitted' not in st.session_state:
    st.session_state_form_submitted = False

with st.form("registration Form", clear_on_submit=False):
    col1,col2 = st.columns(2)

    with col1:
        user_id = st.text_input("User ID *", placeholder="eg: Sharafat123",help="4-20 charecters (letter, number, underscore)")
        full_name= st.text_input("Full Name *",placeholder="eg: Sharafat Hassan",help="2-30 charecters (letter, spaces, hyphens)")
        email=st.text_input("Email *",placeholder="eg: sharafat@email.com",help="Must be Valid ")
    with col2:
        phone=st.text_input("Phone Number *",placeholder="+923000000000",help="Pakistan Format Only")
        password=st.text_input("Password *",placeholder="Enter Your Password",help="8-2 Chars with update,lowercase, number and special charecters")
        confirm_password=st.text_input("Confirm Password *",placeholder="Re-Enter Password")

    submitted=st.form_submit_button("Register Now",use_container_width = True)

#validation and processing

if submitted:
    errors=[]
    warnings = []

    #user_id Validations
    user_id_valid, user_id_msg = validate_user_id(user_id)

    if not user_id_valid:
        errors.append(f"{user_id_msg}")
    elif user_id:
        warnings.append(f"{user_id_msg}")


    #Name Validation
    name_valid,name_msg = validate_name(full_name, "Full name")
    if not full_name:
        errors.append("Full Name Required")
    elif not name_valid:
        errors.append(f"{name_msg}")
    else:
        warnings.append(f"{name_msg}")

    
    #Email Validation
    if not email:
        errors.append("Email Address Required!")
    else:
        email_valid, email_msg = validate_email(email)
        if not email_valid:
            errors.append(f"{email_msg}")
        else:
            warnings.append(f"{email_msg}")

        
        #phone validation
        if not phone:
            errors.append("Phone number is required!")
        else:
            phone_valid,phone_msg=validate_phone(phone)
            if not phone_valid:
                errors.append(f"{phone_msg}")
            else:
                warnings.append(f"{phone_msg}")

        #password validation

        if not password:
            errors.append("Password is required!")
        else:
            password_valid, password_msg = validate_password(password)
            if not password_valid:
                errors.append(f"{password_msg}")
            else:
                warnings.append(f"{password_msg}")

        #confirm password
        if password != confirm_password:
            errors.append("Passwords donot match!")
        elif password and confirm_password:
            warnings.append("Password Match")
            

        #displaying warnings
        if warnings:
            with st.expander("Validations passed!", expanded=False):
                for warning in warnings:
                    st.success(warning)

        
        #displaying errors

        if errors:
            with st.expander("Please Fix the Error:",expanded=True):
                for error in errors:
                    st.error(error)

        else:
            #All validations passed
            if save_user(user_id,full_name,email,phone,password):
                st.snow()
                st.success("Registration Successfull!")
                st.info(f"""
                        Welcome {full_name}!

                        Your Account has been Created Successfully!

                        **Next Step: Please login using your creadentials**
                        """)
                        #ass login button
                if st.button("Go to login page"):  #use st.form_submit_button if not working
                    st.session_state_page="login"
                    st.switch_page("pages/login.py")
            else:
                    st.error("Registration Failed!")
                    
                    